<script lang="ts">
	import { getContext, onMount } from 'svelte';

	import { WEBUI_NAME, mobile, showSidebar } from '$lib/stores';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import SidebarIcon from '$lib/components/icons/Sidebar.svelte';
	import {
		createGtmLoopTaskArtifacts,
		createGtmLoopTaskApproval,
		decideGtmLoopApproval,
		getGtmLoopTaskAudit,
		getGtmLoopTaskApprovals,
		getGtmLoopTasks,
		transitionGtmLoopTask,
		updateGtmLoopTaskStatus,
		type GtmLoopApproval,
		type GtmLoopApprovalCreate,
		type GtmLoopApprovalRisk,
		type GtmLoopApprovalStatus,
		type GtmLoopApprovalType,
		type GtmLoopArtifactLane,
		type GtmLoopTaskAuditEntry,
		type GtmLoopBoardStatus,
		type GtmLoopTask,
		type GtmLoopTaskTransition
	} from '$lib/apis/gtm-loop';
	import { toast } from 'svelte-sonner';

	const i18n = getContext('i18n');

	const columns = [
		{ key: 'planned', label: 'Planned' },
		{ key: 'in-progress', label: 'In Progress' },
		{ key: 'smoke-test', label: 'Smoke Test' },
		{ key: 'in-review', label: 'In Review' },
		{ key: 'done', label: 'Done' }
	] satisfies { key: GtmLoopBoardStatus; label: string }[];
	const cancelledColumn = { key: 'cancelled', label: 'Cancelled' } satisfies {
		key: GtmLoopBoardStatus;
		label: string;
	};
	const statusOptions = [...columns, cancelledColumn];
	const transitionOptions = [
		{ key: 'pick-up', label: 'Pick up task' },
		{ key: 'move-to-ricky', label: 'Send to Ricky' },
		{ key: 'move-to-brody', label: 'Send to Brody' },
		{ key: 'move-to-archy', label: 'Send to Archy' },
		{ key: 'move-to-cody', label: 'Send to Cody' },
		{ key: 'move-to-verifier', label: 'Send to Verifier' },
		{ key: 'move-to-reporter', label: 'Send to Reporter' },
		{ key: 'send-back-for-rework', label: 'Send back for rework' },
		{ key: 'mark-done', label: 'Mark done' }
	] satisfies { key: GtmLoopTaskTransition; label: string }[];
	const laneArtifactOptions = {
		ricky: { lane: 'research', label: 'Create research artifacts' },
		brody: { lane: 'requirements', label: 'Create requirements artifacts' },
		archy: { lane: 'architecture', label: 'Create architecture artifacts' },
		cody: { lane: 'build', label: 'Create build artifacts' },
		verifier: { lane: 'verification', label: 'Create verification artifacts' },
		reporter: { lane: 'report', label: 'Create report artifacts' }
	} satisfies Record<string, { lane: GtmLoopArtifactLane; label: string }>;
	const approvalTypeOptions = [
		'n8n_workflow_create_update',
		'n8n_workflow_activation',
		'hubspot_write',
		'gong_write',
		'airops_write',
		'external_webhook_exposure',
		'email_send',
		'credential_change',
		'dependency_install',
		'destructive_command',
		'production_data_use',
		'client_visible_deliverable',
		'scheduled_loop'
	] satisfies GtmLoopApprovalType[];
	const approvalRiskOptions = ['low', 'medium', 'high', 'critical'] satisfies GtmLoopApprovalRisk[];
	const approvalDecisionOptions = ['approved', 'rejected', 'deferred', 'cancelled'] satisfies Exclude<
		GtmLoopApprovalStatus,
		'requested'
	>[];

	type ApiState = 'loading' | 'loaded' | 'unauthorized' | 'error';
	type AuditState = {
		state: 'idle' | 'loading' | 'loaded' | 'error';
		entries: GtmLoopTaskAuditEntry[];
		error?: string;
	};
	type ApprovalState = {
		state: 'idle' | 'loading' | 'loaded' | 'error';
		approvals: GtmLoopApproval[];
		error?: string;
	};
	type ApprovalDraft = {
		type: GtmLoopApprovalType;
		title: string;
		requested_action: string;
		system: string;
		risk: GtmLoopApprovalRisk;
		evidence_links: string;
		artifact_links: string;
		rollback_plan: string;
		notes: string;
	};

	let tasks: GtmLoopTask[] = [];
	let apiState: ApiState = 'loading';
	let error = '';
	let sourceMode = 'unknown';
	let workspacePath = '';
	let taskCount = 0;
	let lastLoaded = 'Never';
	let searchText = '';
	let clientFilter = '';
	let boardStatusFilter = '';
	let currentLaneFilter = '';
	let priorityFilter = '';
	let blockedFilter = '';
	let approvalRequiredFilter = '';
	let reworkNeededFilter = '';
	let executorFilter = '';
	let verifierFilter = '';
	let tasksByColumn: Record<string, GtmLoopTask[]> = {};
	let visibleColumns = columns;
	let updatingTaskId = '';
	let draggingTaskId = '';
	let dragOverStatus = '';
	let auditByTaskId: Record<string, AuditState> = {};
	let approvalsByTaskId: Record<string, ApprovalState> = {};
	let approvalNotesById: Record<string, string> = {};
	let approvalDraftsByTaskId: Record<string, ApprovalDraft> = {};

	type StringFilterField =
		| 'client'
		| 'board_status'
		| 'current_lane'
		| 'priority'
		| 'executor'
		| 'verifier';

	type TaskFilters = {
		searchText: string;
		clientFilter: string;
		boardStatusFilter: string;
		currentLaneFilter: string;
		priorityFilter: string;
		blockedFilter: string;
		approvalRequiredFilter: string;
		reworkNeededFilter: string;
		executorFilter: string;
		verifierFilter: string;
	};

	const getErrorStatus = (err: unknown) =>
		typeof err === 'object' && err && 'status' in err
			? Number((err as { status?: number }).status ?? 0)
			: 0;

	const getErrorDetail = (err: unknown) =>
		typeof err === 'object' && err && 'detail' in err
			? String((err as { detail?: string }).detail ?? 'Unable to load GTM Loop tasks.')
			: 'Unable to reach the GTM task API.';

	const loadTasks = async () => {
		apiState = 'loading';
		error = '';

		try {
			const response = await getGtmLoopTasks(localStorage.token ?? '');
			tasks = response.tasks ?? [];
			sourceMode = response.source_mode || 'unknown';
			workspacePath = response.workspace_path || '';
			taskCount = response.task_count ?? tasks.length;
			lastLoaded = new Date().toLocaleString();
			apiState = 'loaded';
		} catch (err) {
			tasks = [];
			taskCount = 0;
			if (getErrorStatus(err) === 401) {
				apiState = 'unauthorized';
				error = 'Log in to Open WebUI and refresh the board. The GTM task API is intentionally authenticated.';
			} else {
				apiState = 'error';
				error = getErrorDetail(err);
			}
		}
	};

	const getOptions = (field: StringFilterField) =>
		[...new Set(tasks.map((task) => String(task[field] ?? '').trim()).filter(Boolean))].sort(
			(a, b) => a.localeCompare(b)
		);

	const matchesValue = (value: string | null | undefined, filter: string) =>
		!filter || String(value ?? '') === filter;

	const matchesBoolean = (value: boolean | null | undefined, filter: string) =>
		!filter || String(value === true) === filter;

	const getSearchText = (task: GtmLoopTask) =>
		[
			task.id,
			task.title,
			task.client,
			task.manager_request || task.body_sections?.manager_request,
			task.interpreted_objective || task.body_sections?.interpreted_objective,
			task.next_action || task.body_sections?.next_action,
			task.manager_summary || task.body_sections?.manager_report
		]
			.filter(Boolean)
			.join('\n')
			.toLowerCase();

	const taskMatchesFilters = (task: GtmLoopTask, filters: TaskFilters) => {
		const search = filters.searchText.trim().toLowerCase();
		return (
			(!search || getSearchText(task).includes(search)) &&
			matchesValue(task.client, filters.clientFilter) &&
			matchesValue(task.board_status, filters.boardStatusFilter) &&
			matchesValue(task.current_lane, filters.currentLaneFilter) &&
			matchesValue(task.priority, filters.priorityFilter) &&
			matchesBoolean(task.blocked, filters.blockedFilter) &&
			matchesBoolean(task.approval_required, filters.approvalRequiredFilter) &&
			matchesBoolean(task.rework_needed, filters.reworkNeededFilter) &&
			matchesValue(task.executor, filters.executorFilter) &&
			matchesValue(task.verifier, filters.verifierFilter)
		);
	};

	const clearFilters = () => {
		searchText = '';
		clientFilter = '';
		boardStatusFilter = '';
		currentLaneFilter = '';
		priorityFilter = '';
		blockedFilter = '';
		approvalRequiredFilter = '';
		reworkNeededFilter = '';
		executorFilter = '';
		verifierFilter = '';
	};

	const quickFilterClass = (active: boolean) =>
		active
			? 'bg-black text-white dark:bg-white dark:text-black'
			: 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800';

	const formatLabel = (value = '') => value.replaceAll('-', ' ') || 'none';
	const asList = (value: string[] | null | undefined) => value ?? [];
	const textOrFallback = (value: string | null | undefined, fallback = 'None recorded.') =>
		value && value.trim() ? value : fallback;
	const splitLinks = (value: string) =>
		value
			.split(/[\n,]/)
			.map((link) => link.trim())
			.filter(Boolean);
	const newApprovalDraft = (task: GtmLoopTask): ApprovalDraft => ({
		type: 'n8n_workflow_activation',
		title: `Approve action for ${task.id}`,
		requested_action: '',
		system: 'n8n',
		risk: 'high',
		evidence_links: '',
		artifact_links: asList(task.artifact_links).join('\n'),
		rollback_plan: '',
		notes: ''
	});
	const getApprovalDraft = (task: GtmLoopTask) =>
		approvalDraftsByTaskId[task.id] ?? newApprovalDraft(task);
	const setApprovalDraft = (task: GtmLoopTask, draft: ApprovalDraft) => {
		approvalDraftsByTaskId = { ...approvalDraftsByTaskId, [task.id]: draft };
	};
	const getTaskTransitions = (task: GtmLoopTask) =>
		transitionOptions.filter(({ key }) => {
			if (task.board_status === 'done' || task.board_status === 'cancelled') return false;
			if (task.board_status === 'planned') return key === 'pick-up';
			if (key === 'pick-up') return task.board_status === 'planned';
			if (key === 'mark-done') {
				return (
					!task.blocked &&
					!task.rework_needed &&
					(!task.approval_required || task.approval_status === 'approved') &&
					(task.current_lane === 'reporter' ||
						task.current_lane === 'manager' ||
						task.board_status === 'in-review')
				);
			}
			return key !== 'pick-up';
		});
	const getLaneArtifactOption = (task: GtmLoopTask) => laneArtifactOptions[task.current_lane];

	const loadTaskApprovals = async (taskId: string, force = false) => {
		const current = approvalsByTaskId[taskId];
		if (!force && (current?.state === 'loading' || current?.state === 'loaded')) return;

		approvalsByTaskId = {
			...approvalsByTaskId,
			[taskId]: { state: 'loading', approvals: current?.approvals ?? [] }
		};

		try {
			const response = await getGtmLoopTaskApprovals(localStorage.token ?? '', taskId);
			approvalsByTaskId = {
				...approvalsByTaskId,
				[taskId]: { state: 'loaded', approvals: response.approvals ?? [] }
			};
		} catch (err) {
			approvalsByTaskId = {
				...approvalsByTaskId,
				[taskId]: {
					state: 'error',
					approvals: current?.approvals ?? [],
					error: getErrorDetail(err)
				}
			};
		}
	};

	const loadTaskAudit = async (taskId: string, force = false) => {
		const current = auditByTaskId[taskId];
		if (!force && (current?.state === 'loading' || current?.state === 'loaded')) return;

		auditByTaskId = {
			...auditByTaskId,
			[taskId]: { state: 'loading', entries: current?.entries ?? [] }
		};

		try {
			const response = await getGtmLoopTaskAudit(localStorage.token ?? '', taskId);
			auditByTaskId = {
				...auditByTaskId,
				[taskId]: { state: 'loaded', entries: response.entries ?? [] }
			};
		} catch (err) {
			auditByTaskId = {
				...auditByTaskId,
				[taskId]: { state: 'error', entries: current?.entries ?? [], error: getErrorDetail(err) }
			};
		}
	};

	const updateTaskStatus = async (task: GtmLoopTask, boardStatus: GtmLoopBoardStatus) => {
		if (boardStatus === task.board_status) return;

		updatingTaskId = task.id;
		try {
			const updated = await updateGtmLoopTaskStatus(localStorage.token ?? '', task.id, boardStatus);
			await loadTasks();
			if (auditByTaskId[task.id]?.state === 'loaded') {
				await loadTaskAudit(task.id, true);
			}
			if (updated.audit_warning) {
				toast.warning(`${task.id} moved; ${updated.audit_warning}`);
			} else {
				toast.success(`Moved ${task.id} to ${formatLabel(boardStatus)} and logged audit entry.`);
			}
		} catch (err) {
			toast.error(getErrorDetail(err));
			await loadTasks();
		} finally {
			updatingTaskId = '';
		}
	};

	const startDrag = (event: DragEvent, task: GtmLoopTask) => {
		draggingTaskId = task.id;
		event.dataTransfer?.setData('text/plain', task.id);
		if (event.dataTransfer) event.dataTransfer.effectAllowed = 'move';
	};

	const endDrag = () => {
		draggingTaskId = '';
		dragOverStatus = '';
	};

	const dragOverColumn = (event: DragEvent, boardStatus: GtmLoopBoardStatus) => {
		if (boardStatus === 'cancelled') return;
		event.preventDefault();
		dragOverStatus = boardStatus;
		if (event.dataTransfer) event.dataTransfer.dropEffect = 'move';
	};

	const leaveColumn = (event: DragEvent, boardStatus: GtmLoopBoardStatus) => {
		if (event.currentTarget instanceof HTMLElement && event.relatedTarget instanceof Node) {
			if (event.currentTarget.contains(event.relatedTarget)) return;
		}
		if (dragOverStatus === boardStatus) dragOverStatus = '';
	};

	const dropOnColumn = async (event: DragEvent, boardStatus: GtmLoopBoardStatus) => {
		if (boardStatus === 'cancelled') return;
		event.preventDefault();
		const taskId = event.dataTransfer?.getData('text/plain') || draggingTaskId;
		endDrag();
		const task = tasks.find((candidate) => candidate.id === taskId);
		if (!task || task.board_status === boardStatus) return;
		await updateTaskStatus(task, boardStatus);
	};

	const transitionTask = async (task: GtmLoopTask, transition: GtmLoopTaskTransition) => {
		updatingTaskId = task.id;
		try {
			const updated = await transitionGtmLoopTask(localStorage.token ?? '', task.id, transition);
			await loadTasks();
			if (auditByTaskId[task.id]?.state === 'loaded') {
				await loadTaskAudit(task.id, true);
			}
			if (updated.audit_warning) {
				toast.warning(`${task.id} transitioned; ${updated.audit_warning}`);
			} else {
				toast.success(`Transitioned ${task.id}: ${formatLabel(transition)}.`);
			}
		} catch (err) {
			toast.error(getErrorDetail(err));
		} finally {
			updatingTaskId = '';
		}
	};

	const createLaneArtifacts = async (task: GtmLoopTask) => {
		const option = getLaneArtifactOption(task);
		if (!option) return;

		updatingTaskId = task.id;
		try {
			const updated = await createGtmLoopTaskArtifacts(
				localStorage.token ?? '',
				task.id,
				option.lane
			);
			await loadTasks();

			const created = updated.files_created?.length ?? 0;
			const skipped = updated.files_skipped?.length ?? 0;
			if (updated.audit_warning) {
				toast.warning(`${task.id} artifacts updated; ${updated.audit_warning}`);
			} else if (created > 0) {
				toast.success(`Created ${created} ${formatLabel(option.lane)} artifact${created === 1 ? '' : 's'} for ${task.id}.`);
			} else if (skipped > 0) {
				toast.warning(`${formatLabel(option.lane)} artifacts already exist for ${task.id}; no files overwritten.`);
			}
		} catch (err) {
			toast.error(getErrorDetail(err));
		} finally {
			updatingTaskId = '';
		}
	};

	const createApprovalRequest = async (task: GtmLoopTask) => {
		const draft = getApprovalDraft(task);
		const payload: GtmLoopApprovalCreate = {
			type: draft.type,
			title: draft.title,
			requested_action: draft.requested_action,
			system: draft.system,
			risk: draft.risk,
			evidence_links: splitLinks(draft.evidence_links),
			artifact_links: splitLinks(draft.artifact_links),
			rollback_plan: draft.rollback_plan,
			notes: draft.notes
		};

		updatingTaskId = task.id;
		try {
			const response = await createGtmLoopTaskApproval(localStorage.token ?? '', task.id, payload);
			await loadTasks();
			await loadTaskApprovals(task.id, true);
			setApprovalDraft(task, newApprovalDraft(task));
			if (response.audit_warning) {
				toast.warning(`${response.approval.approval_id} requested; ${response.audit_warning}`);
			} else {
				toast.success(`Requested ${response.approval.approval_id} for ${task.id}.`);
			}
		} catch (err) {
			toast.error(getErrorDetail(err));
		} finally {
			updatingTaskId = '';
		}
	};

	const decideApproval = async (
		task: GtmLoopTask,
		approval: GtmLoopApproval,
		status: Exclude<GtmLoopApprovalStatus, 'requested'>
	) => {
		updatingTaskId = task.id;
		try {
			const response = await decideGtmLoopApproval(
				localStorage.token ?? '',
				approval.approval_id,
				status,
				approvalNotesById[approval.approval_id] ?? ''
			);
			await loadTasks();
			await loadTaskApprovals(task.id, true);
			approvalNotesById = { ...approvalNotesById, [approval.approval_id]: '' };
			if (response.audit_warning) {
				toast.warning(`${approval.approval_id} ${formatLabel(status)}; ${response.audit_warning}`);
			} else {
				toast.success(`${approval.approval_id} ${formatLabel(status)}.`);
			}
		} catch (err) {
			toast.error(getErrorDetail(err));
		} finally {
			updatingTaskId = '';
		}
	};

	const stateClass = (state: ApiState) => {
		if (state === 'loaded') return 'bg-green-100 text-green-700 dark:bg-green-950/40 dark:text-green-200';
		if (state === 'unauthorized')
			return 'bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-200';
		if (state === 'error') return 'bg-red-100 text-red-700 dark:bg-red-950/40 dark:text-red-200';
		return 'bg-gray-100 text-gray-600 dark:bg-gray-850 dark:text-gray-300';
	};

	const flagClass = (flag: 'blocked' | 'approval' | 'rework' | 'priority' | 'lane') => {
		if (flag === 'blocked') return 'bg-red-100 text-red-700 dark:bg-red-950/40 dark:text-red-200';
		if (flag === 'approval')
			return 'bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-200';
		if (flag === 'rework')
			return 'bg-orange-100 text-orange-700 dark:bg-orange-950/40 dark:text-orange-200';
		return 'bg-white text-gray-600 dark:bg-gray-900 dark:text-gray-300';
	};

	$: clientOptions = getOptions('client');
	$: boardStatusOptions = statusOptions.map(({ key }) => key);
	$: currentLaneOptions = getOptions('current_lane');
	$: priorityOptions = getOptions('priority');
	$: executorOptions = getOptions('executor');
	$: verifierOptions = getOptions('verifier');
	$: taskFilters = {
		searchText,
		clientFilter,
		boardStatusFilter,
		currentLaneFilter,
		priorityFilter,
		blockedFilter,
		approvalRequiredFilter,
		reworkNeededFilter,
		executorFilter,
		verifierFilter
	};
	$: filteredTasks = tasks.filter((task) => taskMatchesFilters(task, taskFilters));
	$: visibleColumns = boardStatusFilter === 'cancelled' ? [cancelledColumn] : columns;
	$: tasksByColumn = Object.fromEntries(
		visibleColumns.map(({ key }) => [
			key,
			filteredTasks
				.filter((task) => task.board_status === key)
				.sort((a, b) => a.id.localeCompare(b.id))
		])
	) as Record<string, GtmLoopTask[]>;
	$: activeFilterCount = [
		searchText.trim(),
		clientFilter,
		boardStatusFilter,
		currentLaneFilter,
		priorityFilter,
		blockedFilter,
		approvalRequiredFilter,
		reworkNeededFilter,
		executorFilter,
		verifierFilter
	].filter(Boolean).length;

	onMount(loadTasks);
</script>

<svelte:head>
	<title>GTM Loop Board - {$WEBUI_NAME}</title>
</svelte:head>

<div
	class="flex flex-col w-full h-screen max-h-[100dvh] transition-width duration-200 ease-in-out {$showSidebar
		? 'md:max-w-[calc(100%-var(--sidebar-width))]'
		: ''} max-w-full"
>
	<div class="flex-1 max-h-full overflow-y-auto">
		<div class="mx-auto flex w-full max-w-[96rem] flex-col gap-4 px-3 pb-8 pt-3 md:px-6">
			<div class="flex flex-wrap items-center justify-between gap-3">
				<div class="flex min-w-0 items-center gap-2">
					{#if $mobile}
						<Tooltip content={$showSidebar ? $i18n.t('Close Sidebar') : $i18n.t('Open Sidebar')}>
							<button
								id="sidebar-toggle-button"
								class="cursor-pointer flex rounded-lg hover:bg-gray-100 dark:hover:bg-gray-850 transition"
								on:click={() => {
									showSidebar.set(!$showSidebar);
								}}
								aria-label={$showSidebar ? $i18n.t('Close Sidebar') : $i18n.t('Open Sidebar')}
							>
								<div class="self-center p-1.5">
									<SidebarIcon />
								</div>
							</button>
						</Tooltip>
					{/if}

					<div class="min-w-0">
						<h1 class="truncate text-xl font-medium text-gray-900 dark:text-gray-100">
							{$i18n.t('GTM Loop Board')}
						</h1>
						<div class="truncate text-xs text-gray-500">
							{$i18n.t('Task-file control plane for gtm-loop-workspace/tasks/*.md')}
						</div>
					</div>
				</div>

				<div class="flex flex-wrap gap-2">
					<a
						class="rounded-lg bg-gray-100 px-3 py-2 text-sm font-medium text-gray-800 transition hover:bg-gray-200 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
						href="/gtm-loop"
					>
						{$i18n.t('Cockpit')}
					</a>
					<button
						class="rounded-lg bg-black px-3 py-2 text-sm font-medium text-white transition hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200"
						type="button"
						on:click={loadTasks}
					>
						{$i18n.t('Refresh')}
					</button>
				</div>
			</div>

			<section class="rounded-lg border border-gray-100 bg-white p-3 dark:border-gray-850 dark:bg-gray-900">
				<div class="flex flex-wrap items-center justify-between gap-3">
					<div class="flex flex-wrap gap-2">
						<span class="rounded px-2 py-1 text-xs font-medium {stateClass(apiState)}">
							API: {apiState}
						</span>
						<span class="rounded bg-gray-100 px-2 py-1 text-xs text-gray-600 dark:bg-gray-850 dark:text-gray-300">
							Source: {sourceMode}
						</span>
						<span class="rounded bg-gray-100 px-2 py-1 text-xs text-gray-600 dark:bg-gray-850 dark:text-gray-300">
							Tasks: {taskCount}
						</span>
						<span class="rounded bg-gray-100 px-2 py-1 text-xs text-gray-600 dark:bg-gray-850 dark:text-gray-300">
							Last loaded: {lastLoaded}
						</span>
					</div>
					{#if workspacePath}
						<div class="min-w-0 max-w-full break-all font-mono text-xs text-gray-500">
							{workspacePath}
						</div>
					{/if}
				</div>

				{#if error}
					<div class="mt-3 rounded border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800 dark:border-amber-900/60 dark:bg-amber-950/30 dark:text-amber-200">
						{$i18n.t(error)}
					</div>
				{/if}

				{#if apiState === 'loaded' && taskCount === 0}
					<div class="mt-3 rounded border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800 dark:border-amber-900/60 dark:bg-amber-950/30 dark:text-amber-200">
						{$i18n.t('No tasks found. Run the validator and confirm gtm-loop-workspace/tasks/GTM-*.md exists.')}
					</div>
				{/if}
			</section>

			<section class="rounded-lg border border-gray-100 bg-white p-3 dark:border-gray-850 dark:bg-gray-900">
				<div class="mb-3 flex flex-wrap items-center justify-between gap-3">
					<div>
						<div class="text-sm font-medium text-gray-900 dark:text-gray-100">{$i18n.t('Filters')}</div>
						<div class="mt-0.5 text-xs text-gray-500">
							{filteredTasks.length} / {tasks.length} {$i18n.t('tasks shown')} - {activeFilterCount}
							{$i18n.t('active')}
						</div>
					</div>
					<button
						class="rounded-lg bg-gray-100 px-3 py-2 text-sm font-medium text-gray-800 transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
						type="button"
						disabled={activeFilterCount === 0}
						on:click={clearFilters}
					>
						{$i18n.t('Clear filters')}
					</button>
				</div>

				<div class="grid gap-2 md:grid-cols-2 xl:grid-cols-5">
					<label class="xl:col-span-2">
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Search')}</div>
						<input
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none transition focus:border-gray-300 dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100 dark:focus:border-gray-700"
							bind:value={searchText}
							type="search"
							placeholder={$i18n.t('Search id, title, client, objective, next action...')}
						/>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Client')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={clientFilter}
						>
							<option value="">{$i18n.t('All clients')}</option>
							{#each clientOptions as option}
								<option value={option}>{option}</option>
							{/each}
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Status')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={boardStatusFilter}
						>
							<option value="">{$i18n.t('All statuses')}</option>
							{#each boardStatusOptions as option}
								<option value={option}>{formatLabel(option)}</option>
							{/each}
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Lane')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={currentLaneFilter}
						>
							<option value="">{$i18n.t('All lanes')}</option>
							{#each currentLaneOptions as option}
								<option value={option}>{formatLabel(option)}</option>
							{/each}
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Priority')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={priorityFilter}
						>
							<option value="">{$i18n.t('All priorities')}</option>
							{#each priorityOptions as option}
								<option value={option}>{formatLabel(option)}</option>
							{/each}
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Blocked')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={blockedFilter}
						>
							<option value="">{$i18n.t('Any')}</option>
							<option value="true">{$i18n.t('Yes')}</option>
							<option value="false">{$i18n.t('No')}</option>
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Approval')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={approvalRequiredFilter}
						>
							<option value="">{$i18n.t('Any')}</option>
							<option value="true">{$i18n.t('Required')}</option>
							<option value="false">{$i18n.t('Not required')}</option>
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Rework')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={reworkNeededFilter}
						>
							<option value="">{$i18n.t('Any')}</option>
							<option value="true">{$i18n.t('Needed')}</option>
							<option value="false">{$i18n.t('Not needed')}</option>
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Executor')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={executorFilter}
						>
							<option value="">{$i18n.t('All executors')}</option>
							{#each executorOptions as option}
								<option value={option}>{option}</option>
							{/each}
						</select>
					</label>

					<label>
						<div class="mb-1 text-xs font-medium text-gray-500">{$i18n.t('Verifier')}</div>
						<select
							class="w-full rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm outline-none dark:border-gray-800 dark:bg-gray-850 dark:text-gray-100"
							bind:value={verifierFilter}
						>
							<option value="">{$i18n.t('All verifiers')}</option>
							{#each verifierOptions as option}
								<option value={option}>{option}</option>
							{/each}
						</select>
					</label>
				</div>

				<div class="mt-3 flex flex-wrap gap-2">
					<button
						type="button"
						class="rounded-lg px-2.5 py-1.5 text-xs font-medium transition {quickFilterClass(blockedFilter === 'true')}"
						on:click={() => (blockedFilter = blockedFilter === 'true' ? '' : 'true')}
					>
						{$i18n.t('Blocked')}
					</button>
					<button
						type="button"
						class="rounded-lg px-2.5 py-1.5 text-xs font-medium transition {quickFilterClass(approvalRequiredFilter === 'true')}"
						on:click={() =>
							(approvalRequiredFilter = approvalRequiredFilter === 'true' ? '' : 'true')}
					>
						{$i18n.t('Approval Required')}
					</button>
					<button
						type="button"
						class="rounded-lg px-2.5 py-1.5 text-xs font-medium transition {quickFilterClass(reworkNeededFilter === 'true')}"
						on:click={() => (reworkNeededFilter = reworkNeededFilter === 'true' ? '' : 'true')}
					>
						{$i18n.t('Rework Needed')}
					</button>
					<button
						type="button"
						class="rounded-lg px-2.5 py-1.5 text-xs font-medium transition {quickFilterClass(boardStatusFilter === 'in-review')}"
						on:click={() =>
							(boardStatusFilter = boardStatusFilter === 'in-review' ? '' : 'in-review')}
					>
						{$i18n.t('In Review')}
					</button>
					<button
						type="button"
						class="rounded-lg px-2.5 py-1.5 text-xs font-medium transition {quickFilterClass(boardStatusFilter === 'smoke-test')}"
						on:click={() =>
							(boardStatusFilter = boardStatusFilter === 'smoke-test' ? '' : 'smoke-test')}
					>
						{$i18n.t('Smoke Test')}
					</button>
				</div>
			</section>

			{#if apiState === 'loaded' && tasks.length > 0 && filteredTasks.length === 0}
				<section
					class="rounded-lg border border-amber-200 bg-amber-50 px-3 py-3 text-sm text-amber-800 dark:border-amber-900/60 dark:bg-amber-950/30 dark:text-amber-200"
				>
					<div class="font-medium">{$i18n.t('No matching tasks')}</div>
					<div class="mt-1">
						{$i18n.t('No task cards match the current filters. Clear filters or widen the search.')}
					</div>
				</section>
			{/if}

			{#if apiState === 'loaded'}
				<div class="text-xs text-gray-500">
					{$i18n.t('Drag cards between columns to update board status only. Lane and gate changes stay in card details.')}
				</div>
			{/if}

			<div class="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
				{#each visibleColumns as column}
					<section
						class="flex min-h-[24rem] flex-col rounded-lg border bg-white transition dark:bg-gray-900 {dragOverStatus === column.key
							? 'border-black ring-2 ring-black/10 dark:border-white dark:ring-white/20'
							: 'border-gray-100 dark:border-gray-850'}"
						on:dragover={(event) => dragOverColumn(event, column.key)}
						on:dragenter={(event) => dragOverColumn(event, column.key)}
						on:dragleave={(event) => leaveColumn(event, column.key)}
						on:drop={(event) => dropOnColumn(event, column.key)}
					>
						<div class="flex items-center justify-between border-b border-gray-100 px-3 py-2 dark:border-gray-850">
							<div class="text-sm font-medium text-gray-900 dark:text-gray-100">
								{$i18n.t(column.label)}
							</div>
							<div class="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600 dark:bg-gray-850 dark:text-gray-300">
								{tasksByColumn[column.key]?.length ?? 0}
							</div>
						</div>

						<div class="flex flex-1 flex-col gap-2 p-2">
							{#if apiState === 'loading'}
								<div class="rounded-lg bg-gray-50 px-3 py-2 text-sm text-gray-500 dark:bg-gray-850">
									{$i18n.t('Loading tasks...')}
								</div>
							{:else if apiState !== 'loaded'}
								<div class="rounded-lg bg-gray-50 px-3 py-2 text-sm text-gray-500 dark:bg-gray-850">
									{$i18n.t('Tasks unavailable. Check the board status panel.')}
								</div>
							{:else if (tasksByColumn[column.key]?.length ?? 0) === 0}
								<div class="rounded-lg bg-gray-50 px-3 py-2 text-sm text-gray-500 dark:bg-gray-850">
									{activeFilterCount > 0 ? $i18n.t('No matching tasks') : $i18n.t('No tasks')}
								</div>
							{:else}
								{#each tasksByColumn[column.key] ?? [] as task}
									<article
										class="rounded-lg border border-gray-100 bg-gray-50 p-3 text-sm transition dark:border-gray-800 dark:bg-gray-850 {draggingTaskId === task.id
											? 'opacity-60'
											: 'cursor-grab active:cursor-grabbing'}"
										draggable={updatingTaskId !== task.id}
										on:dragstart={(event) => startDrag(event, task)}
										on:dragend={endDrag}
									>
										<div class="flex items-start justify-between gap-2">
											<div class="min-w-0">
												<div class="font-mono text-xs font-semibold text-gray-500">{task.id}</div>
												<div class="mt-1 text-sm font-medium leading-5 text-gray-900 dark:text-gray-100">
													{task.title}
												</div>
												<div class="mt-1 text-xs text-gray-500">{task.client}</div>
											</div>
											<div class="shrink-0 text-right text-xs text-gray-500">
												<div>{task.progress ?? 0}%</div>
												<div>{task.current_attempt}/{task.max_attempts}</div>
											</div>
										</div>

										<div class="mt-3 flex flex-wrap gap-1">
											<span class="rounded px-2 py-1 text-xs {flagClass('priority')}">
												Priority: {formatLabel(task.priority)}
											</span>
											<span class="rounded px-2 py-1 text-xs {flagClass('lane')}">
												Lane: {formatLabel(task.current_lane)}
											</span>
											{#if task.approval_required}
												<span class="rounded px-2 py-1 text-xs {flagClass('approval')}">
													Approval required
												</span>
											{/if}
											{#if task.blocked}
												<span class="rounded px-2 py-1 text-xs {flagClass('blocked')}">Blocked</span>
											{/if}
											{#if task.rework_needed}
												<span class="rounded px-2 py-1 text-xs {flagClass('rework')}">
													Rework needed
												</span>
											{/if}
										</div>

										<div class="mt-3">
											<label>
												<div class="text-xs font-medium text-gray-500">Move to</div>
												<select
													class="mt-1 w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none disabled:cursor-not-allowed disabled:opacity-60 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
													disabled={updatingTaskId === task.id}
													value={task.board_status}
													on:change={(event) =>
														updateTaskStatus(
															task,
															(event.currentTarget as HTMLSelectElement).value as GtmLoopBoardStatus
														)}
												>
													{#each statusOptions as option}
														<option value={option.key}>{formatLabel(option.key)}</option>
													{/each}
												</select>
											</label>
											{#if updatingTaskId === task.id}
												<div class="mt-1 text-xs text-gray-500">{$i18n.t('Updating status...')}</div>
											{/if}
										</div>

										<div class="mt-3">
											<div class="text-xs font-medium text-gray-500">Next action</div>
											<div class="mt-1 line-clamp-3 text-sm leading-5 text-gray-800 dark:text-gray-200">
												{textOrFallback(task.next_action)}
											</div>
										</div>

										{#if task.manager_summary}
											<div class="mt-3 rounded bg-white px-2 py-2 text-xs leading-5 text-gray-700 dark:bg-gray-900 dark:text-gray-200">
												{task.manager_summary}
											</div>
										{/if}

										<details
											class="mt-3 rounded-lg bg-white dark:bg-gray-900"
											on:toggle={(event) => {
												if ((event.currentTarget as HTMLDetailsElement).open) {
													loadTaskAudit(task.id);
													loadTaskApprovals(task.id);
												}
											}}
										>
											<summary class="cursor-pointer px-2 py-1.5 text-xs font-medium text-gray-700 dark:text-gray-200">
												{$i18n.t('Task card details')}
											</summary>
											<div class="space-y-3 border-t border-gray-100 px-2 py-3 text-xs text-gray-700 dark:border-gray-800 dark:text-gray-200">
												<div class="grid gap-2 sm:grid-cols-2">
													<div>
														<div class="font-medium text-gray-500">Current lane</div>
														<div class="mt-1">{formatLabel(task.current_lane)}</div>
													</div>
													<div>
														<div class="font-medium text-gray-500">Current phase</div>
														<div class="mt-1">{formatLabel(task.current_phase)}</div>
													</div>
													<div>
														<div class="font-medium text-gray-500">Current gate</div>
														<div class="mt-1">{textOrFallback(task.current_gate, 'None')}</div>
													</div>
													<div>
														<div class="font-medium text-gray-500">Approval status</div>
														<div class="mt-1">{formatLabel(task.approval_status)}</div>
													</div>
												</div>

												<div>
													<div class="font-medium text-gray-500">Orchestrator transitions</div>
													<div class="mt-2 flex flex-wrap gap-1.5">
														{#each getTaskTransitions(task) as transition}
															<button
																type="button"
																class="rounded-lg bg-gray-100 px-2.5 py-1.5 text-xs font-medium text-gray-800 transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
																disabled={updatingTaskId === task.id}
																on:click={() => transitionTask(task, transition.key)}
															>
																{transition.label}
															</button>
														{/each}
													</div>
													{#if updatingTaskId === task.id}
														<div class="mt-1 text-xs text-gray-500">{$i18n.t('Updating task...')}</div>
													{/if}
												</div>

												{#if getLaneArtifactOption(task)}
													<div>
														<div class="font-medium text-gray-500">Lane artifacts</div>
														<div class="mt-2">
															<button
																type="button"
																class="rounded-lg bg-gray-100 px-2.5 py-1.5 text-xs font-medium text-gray-800 transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
																disabled={updatingTaskId === task.id}
																on:click={() => createLaneArtifacts(task)}
															>
																{getLaneArtifactOption(task)?.label}
															</button>
														</div>
														<div class="mt-1 text-gray-500">
															Creates local Markdown starters only. Existing files are skipped.
														</div>
													</div>
												{/if}

												<div>
													<div class="font-medium text-gray-500">Approvals</div>
													<div class="mt-1 text-gray-500">
														Local approval records only. Decisions do not execute external actions.
													</div>

													{#if approvalsByTaskId[task.id]?.state === 'loading'}
														<div class="mt-2 rounded bg-gray-50 px-2 py-2 dark:bg-gray-850">
															Loading approvals...
														</div>
													{:else if approvalsByTaskId[task.id]?.state === 'error'}
														<div class="mt-2 rounded border border-amber-200 bg-amber-50 px-2 py-2 text-amber-700 dark:border-amber-900/60 dark:bg-amber-950/30 dark:text-amber-200">
															{approvalsByTaskId[task.id]?.error}
														</div>
													{:else if (approvalsByTaskId[task.id]?.approvals?.length ?? 0) === 0}
														<div class="mt-2 rounded bg-gray-50 px-2 py-2 text-gray-500 dark:bg-gray-850">
															No approvals requested yet.
														</div>
													{:else}
														<div class="mt-2 space-y-2">
															{#each approvalsByTaskId[task.id]?.approvals ?? [] as approval}
																<div class="rounded bg-gray-50 px-2 py-2 dark:bg-gray-850">
																	<div class="flex flex-wrap items-start justify-between gap-2">
																		<div>
																			<div class="font-mono text-[11px] text-gray-500">
																				{approval.approval_id}
																			</div>
																			<div class="mt-1 font-medium">{approval.title}</div>
																		</div>
																		<div class="flex flex-wrap gap-1">
																			<span class="rounded bg-white px-2 py-1 text-[11px] dark:bg-gray-900">
																				{formatLabel(approval.status)}
																			</span>
																			<span class="rounded bg-white px-2 py-1 text-[11px] dark:bg-gray-900">
																				{formatLabel(approval.risk)}
																			</span>
																		</div>
																	</div>
																	<div class="mt-2 grid gap-2 sm:grid-cols-2">
																		<div>
																			<div class="font-medium text-gray-500">Type</div>
																			<div class="mt-1">{formatLabel(approval.type)}</div>
																		</div>
																		<div>
																			<div class="font-medium text-gray-500">System</div>
																			<div class="mt-1">{textOrFallback(approval.system)}</div>
																		</div>
																		<div>
																			<div class="font-medium text-gray-500">Requested by</div>
																			<div class="mt-1">{textOrFallback(approval.requested_by)}</div>
																		</div>
																		<div>
																			<div class="font-medium text-gray-500">Decided by</div>
																			<div class="mt-1">{textOrFallback(approval.decided_by)}</div>
																		</div>
																	</div>
																	<div class="mt-2">
																		<div class="font-medium text-gray-500">Requested action</div>
																		<div class="mt-1">{textOrFallback(approval.requested_action)}</div>
																	</div>
																	<div class="mt-2">
																		<div class="font-medium text-gray-500">Evidence links</div>
																		{#if asList(approval.evidence_links).length}
																			<div class="mt-1 space-y-1">
																				{#each asList(approval.evidence_links) as link}
																					<div class="break-all font-mono">{link}</div>
																				{/each}
																			</div>
																		{:else}
																			<div class="mt-1">None recorded.</div>
																		{/if}
																	</div>
																	<div class="mt-2">
																		<div class="font-medium text-gray-500">Artifact links</div>
																		{#if asList(approval.artifact_links).length}
																			<div class="mt-1 space-y-1">
																				{#each asList(approval.artifact_links) as link}
																					<div class="break-all font-mono">{link}</div>
																				{/each}
																			</div>
																		{:else}
																			<div class="mt-1">None recorded.</div>
																		{/if}
																	</div>
																	<div class="mt-2">
																		<div class="font-medium text-gray-500">Rollback plan</div>
																		<div class="mt-1">{textOrFallback(approval.rollback_plan)}</div>
																	</div>
																	<div class="mt-2">
																		<div class="font-medium text-gray-500">Notes</div>
																		<div class="mt-1">{textOrFallback(approval.notes)}</div>
																	</div>

																	<div class="mt-3">
																		<label>
																			<div class="mb-1 font-medium text-gray-500">Decision note</div>
																			<input
																				class="w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																				type="text"
																				value={approvalNotesById[approval.approval_id] ?? ''}
																				placeholder="Optional short note"
																				on:input={(event) =>
																					(approvalNotesById = {
																						...approvalNotesById,
																						[approval.approval_id]: (
																							event.currentTarget as HTMLInputElement
																						).value
																					})}
																			/>
																		</label>
																		<div class="mt-2 flex flex-wrap gap-1.5">
																			{#each approvalDecisionOptions as decision}
																				<button
																					type="button"
																					class="rounded-lg bg-gray-100 px-2.5 py-1.5 text-xs font-medium text-gray-800 transition hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-gray-900 dark:text-gray-200 dark:hover:bg-gray-800"
																					disabled={updatingTaskId === task.id}
																					on:click={() => decideApproval(task, approval, decision)}
																				>
																					{formatLabel(decision)}
																				</button>
																			{/each}
																		</div>
																	</div>
																</div>
															{/each}
														</div>
													{/if}

													<div class="mt-3 rounded border border-gray-100 bg-gray-50 px-2 py-2 dark:border-gray-800 dark:bg-gray-850">
														<div class="font-medium text-gray-500">Request approval</div>
														<div class="mt-2 grid gap-2 sm:grid-cols-2">
															<label>
																<div class="mb-1 text-gray-500">Type</div>
																<select
																	class="w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																	value={getApprovalDraft(task).type}
																	on:change={(event) =>
																		setApprovalDraft(task, {
																			...getApprovalDraft(task),
																			type: (event.currentTarget as HTMLSelectElement)
																				.value as GtmLoopApprovalType
																		})}
																>
																	{#each approvalTypeOptions as option}
																		<option value={option}>{formatLabel(option)}</option>
																	{/each}
																</select>
															</label>
															<label>
																<div class="mb-1 text-gray-500">Risk</div>
																<select
																	class="w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																	value={getApprovalDraft(task).risk}
																	on:change={(event) =>
																		setApprovalDraft(task, {
																			...getApprovalDraft(task),
																			risk: (event.currentTarget as HTMLSelectElement)
																				.value as GtmLoopApprovalRisk
																		})}
																>
																	{#each approvalRiskOptions as option}
																		<option value={option}>{formatLabel(option)}</option>
																	{/each}
																</select>
															</label>
															<label>
																<div class="mb-1 text-gray-500">Title</div>
																<input
																	class="w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																	type="text"
																	value={getApprovalDraft(task).title}
																	on:input={(event) =>
																		setApprovalDraft(task, {
																			...getApprovalDraft(task),
																			title: (event.currentTarget as HTMLInputElement).value
																		})}
																/>
															</label>
															<label>
																<div class="mb-1 text-gray-500">System</div>
																<input
																	class="w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																	type="text"
																	value={getApprovalDraft(task).system}
																	on:input={(event) =>
																		setApprovalDraft(task, {
																			...getApprovalDraft(task),
																			system: (event.currentTarget as HTMLInputElement).value
																		})}
																/>
															</label>
														</div>
														<label class="mt-2 block">
															<div class="mb-1 text-gray-500">Requested action</div>
															<textarea
																class="min-h-16 w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																value={getApprovalDraft(task).requested_action}
																placeholder="Exact future action this approval would unlock"
																on:input={(event) =>
																	setApprovalDraft(task, {
																		...getApprovalDraft(task),
																		requested_action: (event.currentTarget as HTMLTextAreaElement).value
																	})}
															/>
														</label>
														<label class="mt-2 block">
															<div class="mb-1 text-gray-500">Artifact links</div>
															<textarea
																class="min-h-16 w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 font-mono text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																value={getApprovalDraft(task).artifact_links}
																on:input={(event) =>
																	setApprovalDraft(task, {
																		...getApprovalDraft(task),
																		artifact_links: (event.currentTarget as HTMLTextAreaElement).value
																	})}
															/>
														</label>
														<label class="mt-2 block">
															<div class="mb-1 text-gray-500">Rollback plan</div>
															<textarea
																class="min-h-16 w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																value={getApprovalDraft(task).rollback_plan}
																on:input={(event) =>
																	setApprovalDraft(task, {
																		...getApprovalDraft(task),
																		rollback_plan: (event.currentTarget as HTMLTextAreaElement).value
																	})}
															/>
														</label>
														<label class="mt-2 block">
															<div class="mb-1 text-gray-500">Notes</div>
															<input
																class="w-full rounded-lg border border-gray-100 bg-white px-2 py-1.5 text-xs outline-none dark:border-gray-800 dark:bg-gray-900 dark:text-gray-100"
																type="text"
																value={getApprovalDraft(task).notes}
																on:input={(event) =>
																	setApprovalDraft(task, {
																		...getApprovalDraft(task),
																		notes: (event.currentTarget as HTMLInputElement).value
																	})}
															/>
														</label>
														<button
															type="button"
															class="mt-2 rounded-lg bg-gray-900 px-2.5 py-1.5 text-xs font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-white dark:text-black dark:hover:bg-gray-200"
															disabled={updatingTaskId === task.id || !(approvalDraftsByTaskId[task.id]?.requested_action ?? '').trim()}
															on:click={() => createApprovalRequest(task)}
														>
															Request approval
														</button>
													</div>
												</div>

												<div>
													<div class="font-medium text-gray-500">Manager request</div>
													<div class="mt-1">{textOrFallback(task.manager_request || task.body_sections?.manager_request)}</div>
												</div>
												<div>
													<div class="font-medium text-gray-500">Interpreted objective</div>
													<div class="mt-1">
														{textOrFallback(task.interpreted_objective || task.body_sections?.interpreted_objective)}
													</div>
												</div>
												<div class="grid gap-2 sm:grid-cols-2">
													<div>
														<div class="font-medium text-gray-500">Executor</div>
														<div class="mt-1">{textOrFallback(task.executor)}</div>
													</div>
													<div>
														<div class="font-medium text-gray-500">Verifier</div>
														<div class="mt-1">{textOrFallback(task.verifier)}</div>
													</div>
												</div>
												<div>
													<div class="font-medium text-gray-500">Blocker</div>
													<div class="mt-1">{textOrFallback(task.blocker, 'None')}</div>
												</div>
												<div>
													<div class="font-medium text-gray-500">Definition of done</div>
													<div class="mt-1">
														{textOrFallback(task.definition_of_done || task.body_sections?.definition_of_done)}
													</div>
												</div>
												<div>
													<div class="font-medium text-gray-500">Manager summary</div>
													<div class="mt-1">{textOrFallback(task.manager_summary || task.body_sections?.manager_report)}</div>
												</div>
												<div>
													<div class="font-medium text-gray-500">Evidence links</div>
													{#if asList(task.evidence_links).length}
														<div class="mt-1 space-y-1">
															{#each asList(task.evidence_links) as link}
																<div class="break-all font-mono">{link}</div>
															{/each}
														</div>
													{:else}
														<div class="mt-1">None recorded.</div>
													{/if}
												</div>
												<div>
													<div class="font-medium text-gray-500">Artifact links</div>
													{#if asList(task.artifact_links).length}
														<div class="mt-1 space-y-1">
															{#each asList(task.artifact_links) as link}
																<div class="break-all font-mono">{link}</div>
															{/each}
														</div>
													{:else}
														<div class="mt-1">None recorded.</div>
													{/if}
												</div>
												<div class="grid gap-2 sm:grid-cols-2">
													<div>
														<div class="font-medium text-gray-500">Last updated</div>
														<div class="mt-1">{textOrFallback(task.last_updated)}</div>
													</div>
													<div>
														<div class="font-medium text-gray-500">Source task file</div>
														<div class="mt-1 break-all font-mono">{task.source_path}</div>
													</div>
												</div>
												<div>
													<div class="font-medium text-gray-500">Latest status changes</div>
													{#if auditByTaskId[task.id]?.state === 'loading'}
														<div class="mt-1">Loading status changes...</div>
													{:else if auditByTaskId[task.id]?.state === 'error'}
														<div class="mt-1 text-amber-700 dark:text-amber-300">
															{auditByTaskId[task.id]?.error}
														</div>
													{:else if (auditByTaskId[task.id]?.entries?.length ?? 0) === 0}
														<div class="mt-1">No status changes logged yet.</div>
													{:else}
														<div class="mt-1 space-y-2">
															{#each auditByTaskId[task.id]?.entries ?? [] as entry}
																<div class="rounded bg-gray-50 px-2 py-2 dark:bg-gray-850">
																	<div class="font-mono text-[11px] text-gray-500">{entry.timestamp}</div>
																	{#if entry.transition}
																		<div class="mt-1 font-medium">
																			{formatLabel(entry.transition)}
																		</div>
																	{/if}
																	<div class="mt-1">
																		{formatLabel(entry.old_board_status)} -> {formatLabel(
																			entry.new_board_status
																		)}
																	</div>
																	{#if entry.new_lane || entry.new_phase || entry.new_gate}
																		<div class="mt-1 text-gray-500">
																			{formatLabel(entry.old_lane)} -> {formatLabel(entry.new_lane)}
																			/ {formatLabel(entry.new_phase || entry.new_gate)}
																		</div>
																	{/if}
																	<div class="mt-1 text-gray-500">
																		{textOrFallback(entry.actor, 'Unknown actor')} via
																		{textOrFallback(entry.source, 'unknown source')}
																	</div>
																</div>
															{/each}
														</div>
													{/if}
												</div>
											</div>
										</details>
									</article>
								{/each}
							{/if}
						</div>
					</section>
				{/each}
			</div>
		</div>
	</div>
</div>
