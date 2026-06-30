#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const tasksDir = path.join(root, 'gtm-loop-workspace', 'tasks');
const boardPath = path.join(root, 'gtm-loop-workspace', 'board.md');

const requiredFields = [
	'gtm_task',
	'id',
	'title',
	'client',
	'board_status',
	'current_lane',
	'current_gate',
	'current_phase',
	'priority',
	'progress',
	'manager_request',
	'interpreted_objective',
	'executor',
	'verifier',
	'approval_required',
	'approval_status',
	'blocked',
	'rework_needed',
	'proposal_required',
	'architecture_required',
	'current_attempt',
	'max_attempts',
	'artifact_links',
	'evidence_links',
	'next_action',
	'definition_of_done',
	'manager_summary',
	'last_updated'
];

const booleanFields = [
	'gtm_task',
	'approval_required',
	'blocked',
	'rework_needed',
	'proposal_required',
	'architecture_required'
];

const numericFields = ['progress', 'current_attempt', 'max_attempts'];
const listFields = ['dependencies', 'tags', 'artifact_links', 'evidence_links'];

const allowed = {
	board_status: new Set(['planned', 'in-progress', 'smoke-test', 'in-review', 'done', 'cancelled']),
	current_lane: new Set(['ricky', 'brody', 'archy', 'cody', 'verifier', 'reporter', 'manager', 'none']),
	approval_status: new Set(['not_required', 'required', 'requested', 'approved', 'rejected', 'deferred']),
	priority: new Set(['low', 'medium', 'high', 'urgent']),
	current_phase: new Set([
		'intake',
		'triage',
		'context-read',
		'research',
		'requirements',
		'proposal',
		'architecture',
		'execution-plan',
		'build',
		'verify',
		'rework',
		'smoke-test',
		'report',
		'board-update',
		'done'
	])
};

const boardSections = new Map([
	['planned', 'Planned'],
	['in-progress', 'In Progress'],
	['smoke-test', 'Smoke Test'],
	['in-review', 'In Review'],
	['done', 'Done']
]);

const secretPattern = /(api_key|token|secret|password|bearer|private_key|client_secret|refresh_token|access_token)/i;

const errors = [];
const warnings = [];

function rel(filePath) {
	return path.relative(root, filePath).replaceAll(path.sep, '/');
}

function addError(filePath, message) {
	errors.push(`${rel(filePath)}: ${message}`);
}

function addWarning(filePath, message) {
	warnings.push(`${rel(filePath)}: ${message}`);
}

function parseScalar(raw) {
	const value = raw.trim();
	if (value === 'true') return true;
	if (value === 'false') return false;
	if (/^-?\d+$/.test(value)) return Number.parseInt(value, 10);
	if (value === '[]') return [];
	if (value.startsWith('[') && value.endsWith(']')) {
		const body = value.slice(1, -1).trim();
		if (!body) return [];
		return body.split(',').map((part) => parseScalar(part.trim()));
	}
	if (
		(value.startsWith('"') && value.endsWith('"')) ||
		(value.startsWith("'") && value.endsWith("'"))
	) {
		return value.slice(1, -1);
	}
	return value;
}

function parseFrontmatter(filePath) {
	const text = fs.readFileSync(filePath, 'utf8');
	if (!text.startsWith('---\n') && !text.startsWith('---\r\n')) {
		addError(filePath, 'missing opening frontmatter delimiter');
		return null;
	}

	const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
	if (!match) {
		addError(filePath, 'missing closing frontmatter delimiter');
		return null;
	}

	const data = {};
	for (const [index, line] of match[1].split(/\r?\n/).entries()) {
		const trimmed = line.trim();
		if (!trimmed || trimmed.startsWith('#')) continue;
		const field = line.match(/^([A-Za-z0-9_-]+):(?:\s*(.*))?$/);
		if (!field) {
			addError(filePath, `unsupported frontmatter line ${index + 2}: ${line}`);
			continue;
		}
		const key = field[1];
		data[key] = parseScalar(field[2] ?? '');
	}
	return data;
}

function validateTask(filePath, allTasks) {
	const fileName = path.basename(filePath);
	const expectedId = fileName.replace(/\.md$/, '');
	const frontmatter = parseFrontmatter(filePath);
	if (!frontmatter) return null;

	for (const field of requiredFields) {
		if (!(field in frontmatter)) addError(filePath, `missing required field "${field}"`);
	}

	if (frontmatter.id !== expectedId) {
		addError(filePath, `id "${frontmatter.id}" does not match filename "${expectedId}"`);
	}

	for (const [field, values] of Object.entries(allowed)) {
		if (field in frontmatter && !values.has(frontmatter[field])) {
			addError(filePath, `${field} "${frontmatter[field]}" is not allowed`);
		}
	}

	for (const field of booleanFields) {
		if (field in frontmatter && typeof frontmatter[field] !== 'boolean') {
			addError(filePath, `${field} must be a boolean`);
		}
	}

	for (const field of numericFields) {
		if (field in frontmatter && (!Number.isInteger(frontmatter[field]) || Number.isNaN(frontmatter[field]))) {
			addError(filePath, `${field} must be an integer`);
		}
	}

	if (Number.isInteger(frontmatter.progress) && (frontmatter.progress < 0 || frontmatter.progress > 100)) {
		addError(filePath, 'progress must be between 0 and 100');
	}

	if (
		Number.isInteger(frontmatter.current_attempt) &&
		Number.isInteger(frontmatter.max_attempts) &&
		frontmatter.current_attempt > frontmatter.max_attempts
	) {
		addError(filePath, `current_attempt ${frontmatter.current_attempt} exceeds max_attempts ${frontmatter.max_attempts}`);
	}

	for (const field of listFields) {
		if (field in frontmatter && !Array.isArray(frontmatter[field])) {
			addError(filePath, `${field} must be a list`);
		}
	}

	for (const [key, value] of Object.entries(frontmatter)) {
		if (secretPattern.test(key)) {
			addError(filePath, `suspicious credential-style frontmatter key "${key}"`);
		}
		const values = Array.isArray(value) ? value : [value];
		for (const item of values) {
			if (typeof item === 'string' && secretPattern.test(item)) {
				addWarning(filePath, `suspicious credential-style frontmatter value in "${key}"`);
			}
		}
	}

	if (frontmatter.gtm_task !== true) addError(filePath, 'gtm_task must be true');
	if (!frontmatter.title) addWarning(filePath, 'title is empty');
	if (!frontmatter.client) addWarning(filePath, 'client is empty');
	if (!frontmatter.next_action) addWarning(filePath, 'next_action is empty');

	allTasks.set(expectedId, { filePath, frontmatter });
	return frontmatter;
}

function parseBoard() {
	if (!fs.existsSync(boardPath)) {
		addError(boardPath, 'board.md is missing');
		return { entries: [], sections: [] };
	}

	const text = fs.readFileSync(boardPath, 'utf8');
	const entries = [];
	const sections = [];
	let currentSection = null;

	for (const [index, line] of text.split(/\r?\n/).entries()) {
		const section = line.match(/^##\s+(.+?)\s*$/);
		if (section) {
			currentSection = section[1];
			sections.push(currentSection);
			if (![...boardSections.values()].includes(currentSection)) {
				addError(boardPath, `unexpected board section "${currentSection}" on line ${index + 1}`);
			}
			continue;
		}

		const link = line.match(/\[([A-Z]+-\d+)\]\((tasks\/([A-Z]+-\d+)\.md)\)/);
		if (link) {
			const [, labelId, href, fileId] = link;
			if (labelId !== fileId) {
				addError(boardPath, `line ${index + 1} label "${labelId}" does not match link "${href}"`);
			}
			entries.push({ id: labelId, href, section: currentSection, line: index + 1 });
		}
	}

	for (const required of boardSections.values()) {
		if (!sections.includes(required)) addError(boardPath, `missing board section "${required}"`);
	}

	return { entries, sections };
}

function validateBoard(tasks) {
	const board = parseBoard();
	const seen = new Set();

	for (const entry of board.entries) {
		const taskPath = path.join(root, 'gtm-loop-workspace', entry.href);
		if (!fs.existsSync(taskPath)) {
			addError(boardPath, `line ${entry.line} references missing task file "${entry.href}"`);
			continue;
		}

		seen.add(entry.id);
		const task = tasks.get(entry.id);
		if (!task) continue;

		const expectedSection = boardSections.get(task.frontmatter.board_status);
		if (expectedSection && entry.section !== expectedSection) {
			addWarning(
				boardPath,
				`${entry.id} appears under "${entry.section}" but board_status "${task.frontmatter.board_status}" maps to "${expectedSection}"`
			);
		}
	}

	for (const [id, task] of tasks) {
		if (task.frontmatter.board_status === 'cancelled') continue;
		if (!seen.has(id)) {
			addError(boardPath, `${id} is not listed in board.md`);
		}
	}
}

function main() {
	if (!fs.existsSync(tasksDir)) {
		addError(tasksDir, 'tasks directory is missing');
	} else {
		const taskFiles = fs
			.readdirSync(tasksDir)
			.filter((name) => /^GTM-\d+\.md$/.test(name))
			.sort()
			.map((name) => path.join(tasksDir, name));

		const tasks = new Map();
		for (const filePath of taskFiles) validateTask(filePath, tasks);
		validateBoard(tasks);

		console.log(`GTM task validation checked ${taskFiles.length} task file(s).`);
	}

	if (warnings.length) {
		console.log(`\nWarnings (${warnings.length}):`);
		for (const warning of warnings) console.log(`  - ${warning}`);
	}

	if (errors.length) {
		console.log(`\nErrors (${errors.length}):`);
		for (const error of errors) console.log(`  - ${error}`);
		console.log('\nFAIL');
		process.exit(1);
	}

	console.log('\nErrors: 0');
	console.log(`Warnings: ${warnings.length}`);
	console.log('PASS');
}

main();
