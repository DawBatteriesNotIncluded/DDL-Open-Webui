import { WEBUI_BASE_URL } from '$lib/constants';

export type GtmLoopTask = {
	gtm_task: boolean;
	id: string;
	title: string;
	client: string;
	board_status: 'planned' | 'in-progress' | 'smoke-test' | 'in-review' | 'done' | 'cancelled';
	current_lane: string;
	current_gate: string;
	current_phase: string;
	priority: string;
	progress: number;
	manager_request: string;
	interpreted_objective: string;
	executor: string;
	verifier: string;
	approval_required: boolean;
	approval_status: string;
	blocked: boolean;
	blocker: string;
	rework_needed: boolean;
	proposal_required: boolean;
	architecture_required: boolean;
	current_attempt: number;
	max_attempts: number;
	dependencies: string[];
	tags: string[];
	artifact_links: string[];
	evidence_links: string[];
	next_action: string;
	definition_of_done: string;
	manager_summary: string;
	last_updated: string;
	source_path: string;
	body_sections: Record<string, string>;
};

export type GtmLoopTasksResponse = {
	tasks: GtmLoopTask[];
	counts: {
		total: number;
		blocked: number;
		approval_required: number;
		in_review: number;
	};
	columns: Record<string, string[]>;
	workspace_path: string;
	task_count: number;
	source_mode: string;
};

export type GtmLoopApiError = {
	status: number;
	detail: string;
};

export const getGtmLoopTasks = async (token: string = ''): Promise<GtmLoopTasksResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to load GTM Loop tasks.';
		try {
			const body = await res.json();
			detail = body.detail ?? detail;
		} catch {
			// Keep the status text fallback.
		}

		throw { status: res.status, detail } satisfies GtmLoopApiError;
	}

	return res.json();
};
