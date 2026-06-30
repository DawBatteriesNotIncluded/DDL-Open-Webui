<script lang="ts">
	import { getContext, onMount } from 'svelte';

	import { WEBUI_NAME, mobile, showSidebar } from '$lib/stores';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import SidebarIcon from '$lib/components/icons/Sidebar.svelte';
	import { getGtmLoopTasks, type GtmLoopTask } from '$lib/apis/gtm-loop';

	const i18n = getContext('i18n');

	const columns = [
		{ key: 'planned', label: 'Planned' },
		{ key: 'in-progress', label: 'In Progress' },
		{ key: 'smoke-test', label: 'Smoke Test' },
		{ key: 'in-review', label: 'In Review' },
		{ key: 'done', label: 'Done' }
	];

	type ApiState = 'loading' | 'loaded' | 'unauthorized' | 'error';

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
	$: boardStatusOptions = getOptions('board_status');
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
	$: tasksByColumn = Object.fromEntries(
		columns.map(({ key }) => [
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
							{$i18n.t('Read-only view of gtm-loop-workspace/tasks/*.md')}
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

			<div class="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
				{#each columns as column}
					<section
						class="flex min-h-[24rem] flex-col rounded-lg border border-gray-100 bg-white dark:border-gray-850 dark:bg-gray-900"
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
										class="rounded-lg border border-gray-100 bg-gray-50 p-3 text-sm dark:border-gray-800 dark:bg-gray-850"
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

										<details class="mt-3 rounded-lg bg-white dark:bg-gray-900">
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
