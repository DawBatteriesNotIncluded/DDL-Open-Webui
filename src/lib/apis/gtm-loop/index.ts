import { WEBUI_BASE_URL } from '$lib/constants';

export type GtmLoopBoardStatus =
	| 'planned'
	| 'in-progress'
	| 'smoke-test'
	| 'in-review'
	| 'done'
	| 'cancelled';

export type GtmLoopTask = {
	gtm_task: boolean;
	id: string;
	title: string;
	client: string;
	board_status: GtmLoopBoardStatus;
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

export type GtmLoopTaskStatusResponse = GtmLoopTask & {
	audit_logged?: boolean;
	audit_warning?: string;
};

export type GtmLoopTaskTransition =
	| 'pick-up'
	| 'move-to-ricky'
	| 'move-to-brody'
	| 'move-to-archy'
	| 'move-to-cody'
	| 'move-to-verifier'
	| 'move-to-reporter'
	| 'send-back-for-rework'
	| 'mark-done';

export type GtmLoopTaskTransitionResponse = GtmLoopTask & {
	audit_logged?: boolean;
	audit_warning?: string;
};

export type GtmLoopArtifactLane =
	| 'research'
	| 'requirements'
	| 'architecture'
	| 'build'
	| 'verification'
	| 'report';

export type GtmLoopTaskArtifactsResponse = GtmLoopTask & {
	files_created: string[];
	files_skipped: string[];
	audit_logged?: boolean;
	audit_warning?: string;
};

export type GtmLoopTaskAuditEntry = {
	timestamp: string;
	task_id: string;
	old_board_status: string;
	new_board_status: string;
	transition: string;
	old_lane: string;
	new_lane: string;
	old_phase: string;
	new_phase: string;
	old_gate: string;
	new_gate: string;
	actor: string;
	source: string;
	endpoint: string;
	success: boolean;
};

export type GtmLoopTaskAuditResponse = {
	task_id: string;
	entries: GtmLoopTaskAuditEntry[];
};

export type GtmLoopApprovalType =
	| 'n8n_workflow_create_update'
	| 'n8n_workflow_activation'
	| 'hubspot_write'
	| 'gong_write'
	| 'airops_write'
	| 'external_webhook_exposure'
	| 'email_send'
	| 'credential_change'
	| 'dependency_install'
	| 'destructive_command'
	| 'production_data_use'
	| 'client_visible_deliverable'
	| 'scheduled_loop';

export type GtmLoopApprovalStatus =
	| 'requested'
	| 'approved'
	| 'rejected'
	| 'deferred'
	| 'cancelled';

export type GtmLoopApprovalRisk = 'low' | 'medium' | 'high' | 'critical';

export type GtmLoopApproval = {
	approval_id: string;
	task_id: string;
	type: GtmLoopApprovalType;
	title: string;
	requested_action: string;
	system: string;
	risk: GtmLoopApprovalRisk;
	status: GtmLoopApprovalStatus;
	requested_by: string;
	decided_by: string;
	created_at: string;
	updated_at: string;
	evidence_links: string[];
	artifact_links: string[];
	rollback_plan: string;
	notes: string;
};

export type GtmLoopApprovalCounts = {
	total: number;
	requested: number;
	approved: number;
	rejected: number;
	deferred: number;
	critical_high_requested: number;
};

export type GtmLoopApprovalsResponse = {
	approvals: GtmLoopApproval[];
	counts: GtmLoopApprovalCounts;
	count: number;
	task_id?: string;
};

export type GtmLoopApprovalCreate = {
	type: GtmLoopApprovalType;
	title: string;
	requested_action: string;
	system: string;
	risk: GtmLoopApprovalRisk;
	evidence_links?: string[];
	artifact_links?: string[];
	rollback_plan?: string;
	notes?: string;
};

export type GtmLoopApprovalResponse = {
	approval: GtmLoopApproval;
	task: GtmLoopTask;
	audit_logged?: boolean;
	audit_warning?: string;
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

export const getGtmLoopApprovals = async (
	token: string = '',
	filters: Record<string, string> = {}
): Promise<GtmLoopApprovalsResponse> => {
	const params = new URLSearchParams();
	for (const [key, value] of Object.entries(filters)) {
		if (value) params.set(key, value);
	}
	const query = params.toString();
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/approvals${query ? `?${query}` : ''}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to load GTM approvals.';
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

export const getGtmLoopTaskApprovals = async (
	token: string,
	taskId: string
): Promise<GtmLoopApprovalsResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/approvals`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to load GTM task approvals.';
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

export const createGtmLoopTaskApproval = async (
	token: string,
	taskId: string,
	approval: GtmLoopApprovalCreate
): Promise<GtmLoopApprovalResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/approvals`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify(approval)
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to create GTM approval.';
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

export const decideGtmLoopApproval = async (
	token: string,
	approvalId: string,
	status: Exclude<GtmLoopApprovalStatus, 'requested'>,
	notes: string = ''
): Promise<GtmLoopApprovalResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/approvals/${approvalId}/decision`, {
		method: 'PATCH',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ status, notes })
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to update GTM approval.';
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

export const updateGtmLoopTaskStatus = async (
	token: string,
	taskId: string,
	boardStatus: GtmLoopBoardStatus
): Promise<GtmLoopTaskStatusResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/status`, {
		method: 'PATCH',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ board_status: boardStatus })
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to update GTM task status.';
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

export const transitionGtmLoopTask = async (
	token: string,
	taskId: string,
	transition: GtmLoopTaskTransition
): Promise<GtmLoopTaskTransitionResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/transition`, {
		method: 'PATCH',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ transition })
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to transition GTM task.';
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

export const createGtmLoopTaskArtifacts = async (
	token: string,
	taskId: string,
	lane: GtmLoopArtifactLane,
	overwrite: boolean = false
): Promise<GtmLoopTaskArtifactsResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/artifacts/${lane}`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ overwrite })
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to create GTM task artifacts.';
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

export const createGtmLoopTaskN8nDraft = async (
	token: string,
	taskId: string,
	overwrite: boolean = false
): Promise<GtmLoopTaskArtifactsResponse> => {
	const res = await fetch(`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/n8n-draft`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ overwrite })
	});

	if (!res.ok) {
		let detail = res.statusText || 'Unable to create GTM n8n workflow draft.';
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

export const getGtmLoopTaskAudit = async (
	token: string,
	taskId: string,
	limit: number = 3
): Promise<GtmLoopTaskAuditResponse> => {
	const res = await fetch(
		`${WEBUI_BASE_URL}/api/gtm-loop/tasks/${taskId}/audit?limit=${encodeURIComponent(limit)}`,
		{
			method: 'GET',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				authorization: `Bearer ${token}`
			}
		}
	);

	if (!res.ok) {
		let detail = res.statusText || 'Unable to load GTM task audit.';
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
