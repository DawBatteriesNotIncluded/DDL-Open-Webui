<script lang="ts">
	import { getContext, onMount } from 'svelte';

	import { WEBUI_NAME, mobile, showSidebar } from '$lib/stores';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import SidebarIcon from '$lib/components/icons/Sidebar.svelte';
	import { getGtmLoopTasks, type GtmLoopTasksResponse } from '$lib/apis/gtm-loop';

	const i18n = getContext('i18n');

	const statusRows = [
		{ label: 'Active client', value: 'TBD' },
		{ label: 'Active task', value: 'GTM-001' },
		{ label: 'Lane', value: 'Brody' },
		{ label: 'Readiness', value: 'Blocked on manager input' },
		{ label: 'Knowledge pack', value: 'GTM Workbench Core Pack' },
		{ label: 'Approval mode', value: 'Manual approval for external writes' }
	];

	let taskSummaryRows = [
		{ label: 'Total tasks', value: '...' },
		{ label: 'Planned', value: '...' },
		{ label: 'In progress', value: '...' },
		{ label: 'Smoke test', value: '...' },
		{ label: 'In review', value: '...' },
		{ label: 'Done', value: '...' },
		{ label: 'Blocked', value: '...' },
		{ label: 'Approval required', value: '...' },
		{ label: 'Source mode', value: '...' }
	];
	let taskSummaryError = '';

	const nextActions = [
		'Confirm the first real client and initial automation objective.',
		'Create the client folder from gtm-loop-workspace/clients/onboarding.md.',
		'Update tasks/GTM-001.md, then mirror board.md.'
	];

	const openWebUILinks = [
		{ label: 'Kanban Board', href: '/gtm-loop/board' },
		{ label: 'Models', href: '/workspace/models' },
		{ label: 'Knowledge', href: '/workspace/knowledge' },
		{ label: 'Automations', href: '/automations' },
		{ label: 'Workspace', href: '/workspace' }
	];

	const sourceFiles = [
		'gtm-loop-workspace/HOME.md',
		'gtm-loop-workspace/workbench.md',
		'gtm-loop-workspace/tasks/',
		'gtm-loop-workspace/board.md',
		'gtm-loop-workspace/openwebui-knowledge-packs.md',
		'gtm-loop-workspace/clients/onboarding.md'
	];

	const safetyGates = [
		'No secrets or raw customer records in Knowledge.',
		'No API writes without explicit approval.',
		'No workflow activation without validation notes.',
		'Use fake or redacted payloads for examples.'
	];

	const starterPrompt = `Start GTM Loop for first client onboarding.

Use gtm-loop-workspace/HOME.md and gtm-loop-workspace/workbench.md as control files.
Current task: GTM-001.
Current lane: Brody.

Separate evidence into confirmed, mismatch, unknown, inferred, and recommendation.
Do not write to external systems or activate workflows without explicit approval.`;

	let copiedPrompt = false;

	const copyStarterPrompt = async () => {
		await navigator.clipboard.writeText(starterPrompt);
		copiedPrompt = true;
		setTimeout(() => {
			copiedPrompt = false;
		}, 1600);
	};

	const countColumn = (response: GtmLoopTasksResponse, status: string) =>
		(response.columns?.[status] ?? []).length.toString();

	onMount(async () => {
		try {
			const response = await getGtmLoopTasks(localStorage.token);
			taskSummaryRows = [
				{ label: 'Total tasks', value: (response.task_count ?? response.counts.total).toString() },
				{ label: 'Planned', value: countColumn(response, 'planned') },
				{ label: 'In progress', value: countColumn(response, 'in-progress') },
				{ label: 'Smoke test', value: countColumn(response, 'smoke-test') },
				{ label: 'In review', value: countColumn(response, 'in-review') },
				{ label: 'Done', value: countColumn(response, 'done') },
				{ label: 'Blocked', value: response.counts.blocked.toString() },
				{ label: 'Approval required', value: response.counts.approval_required.toString() },
				{ label: 'Source mode', value: response.source_mode || 'unknown' }
			];
		} catch (err) {
			taskSummaryError =
				typeof err === 'object' && err && 'detail' in err
					? String(err.detail)
					: 'Unable to load GTM Loop task summary.';
		}
	});
</script>

<svelte:head>
	<title>GTM Loop - {$WEBUI_NAME}</title>
</svelte:head>

<div
	class="flex flex-col w-full h-screen max-h-[100dvh] transition-width duration-200 ease-in-out {$showSidebar
		? 'md:max-w-[calc(100%-var(--sidebar-width))]'
		: ''} max-w-full"
>
	<div class="flex-1 max-h-full overflow-y-auto">
		<div class="mx-auto flex w-full max-w-6xl flex-col gap-4 px-3 pb-8 pt-3 md:px-6">
			<div class="flex items-center justify-between gap-3">
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
							{$i18n.t('GTM Loop')}
						</h1>
						<div class="truncate text-xs text-gray-500">
							{$i18n.t('Active client TBD / task GTM-001 / Brody lane')}
						</div>
					</div>
				</div>

				<div class="flex flex-wrap gap-2">
					<a
						class="rounded-lg bg-gray-100 px-3 py-2 text-sm font-medium text-gray-800 transition hover:bg-gray-200 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
						href="/gtm-loop/board"
					>
						{$i18n.t('Open Kanban Board')}
					</a>
					<a
						class="rounded-lg bg-black px-3 py-2 text-sm font-medium text-white transition hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200"
						href="/workspace/models"
					>
						{$i18n.t('Open Agent')}
					</a>
				</div>
			</div>

			<section
				class="rounded-2xl border border-gray-100 bg-white p-4 dark:border-gray-850 dark:bg-gray-900"
			>
				<div class="mb-3 text-sm font-medium text-gray-900 dark:text-gray-100">
					{$i18n.t('Today')}
				</div>

				<div class="grid gap-2 md:grid-cols-2 xl:grid-cols-3">
					{#each statusRows as row}
						<div class="rounded-xl bg-gray-50 px-3 py-2 dark:bg-gray-850">
							<div class="text-xs text-gray-500">{$i18n.t(row.label)}</div>
							<div class="mt-0.5 text-sm font-medium text-gray-900 dark:text-gray-100">
								{$i18n.t(row.value)}
							</div>
						</div>
					{/each}
				</div>

				<div class="mt-4 grid gap-2 md:grid-cols-3 xl:grid-cols-5">
					{#each taskSummaryRows as row}
						<div class="rounded-lg bg-gray-50 px-3 py-2 dark:bg-gray-850">
							<div class="text-xs text-gray-500">{$i18n.t(row.label)}</div>
							<div class="mt-0.5 text-sm font-medium text-gray-900 dark:text-gray-100">
								{$i18n.t(row.value)}
							</div>
						</div>
					{/each}
				</div>

				{#if taskSummaryError}
					<div class="mt-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700 dark:border-amber-900/60 dark:bg-amber-950/30 dark:text-amber-200">
						{$i18n.t(taskSummaryError)}
					</div>
				{/if}
			</section>

			<div class="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
				<section
					class="rounded-2xl border border-gray-100 bg-white p-4 dark:border-gray-850 dark:bg-gray-900"
				>
					<div class="mb-3 text-sm font-medium text-gray-900 dark:text-gray-100">
						{$i18n.t('Next Actions')}
					</div>

					<div class="space-y-2">
						{#each nextActions as action, index}
							<div class="flex gap-3 rounded-xl bg-gray-50 px-3 py-2 dark:bg-gray-850">
								<div class="text-xs font-medium text-gray-500">{index + 1}</div>
								<div class="text-sm text-gray-800 dark:text-gray-200">{$i18n.t(action)}</div>
							</div>
						{/each}
					</div>
				</section>

				<section
					class="rounded-2xl border border-gray-100 bg-white p-4 dark:border-gray-850 dark:bg-gray-900"
				>
					<div class="mb-3 text-sm font-medium text-gray-900 dark:text-gray-100">
						{$i18n.t('Open In Open WebUI')}
					</div>

					<div class="grid grid-cols-2 gap-2">
						{#each openWebUILinks as link}
							<a
								class="rounded-xl bg-gray-50 px-3 py-2 text-center text-sm font-medium text-gray-800 transition hover:bg-gray-100 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
								href={link.href}
							>
								{$i18n.t(link.label)}
							</a>
						{/each}
					</div>
				</section>
			</div>

			<div class="grid gap-4 lg:grid-cols-2">
				<section
					class="rounded-2xl border border-gray-100 bg-white p-4 dark:border-gray-850 dark:bg-gray-900"
				>
					<div class="mb-3 flex items-center justify-between gap-2">
						<div class="text-sm font-medium text-gray-900 dark:text-gray-100">
							{$i18n.t('Starter Prompt')}
						</div>
						<button
							class="rounded-lg bg-gray-100 px-2.5 py-1.5 text-xs font-medium text-gray-800 transition hover:bg-gray-200 dark:bg-gray-850 dark:text-gray-200 dark:hover:bg-gray-800"
							type="button"
							on:click={copyStarterPrompt}
						>
							{copiedPrompt ? $i18n.t('Copied') : $i18n.t('Copy')}
						</button>
					</div>

					<pre
						class="max-h-72 overflow-auto whitespace-pre-wrap rounded-xl bg-gray-50 p-3 text-xs leading-5 text-gray-700 dark:bg-gray-850 dark:text-gray-200">{starterPrompt}</pre>
				</section>

				<section
					class="rounded-2xl border border-gray-100 bg-white p-4 dark:border-gray-850 dark:bg-gray-900"
				>
					<div class="mb-3 text-sm font-medium text-gray-900 dark:text-gray-100">
						{$i18n.t('Safety Gates')}
					</div>

					<div class="space-y-2">
						{#each safetyGates as gate}
							<div class="rounded-xl bg-gray-50 px-3 py-2 text-sm text-gray-800 dark:bg-gray-850 dark:text-gray-200">
								{$i18n.t(gate)}
							</div>
						{/each}
					</div>
				</section>
			</div>

			<section
				class="rounded-2xl border border-gray-100 bg-white p-4 dark:border-gray-850 dark:bg-gray-900"
			>
				<div class="mb-3 text-sm font-medium text-gray-900 dark:text-gray-100">
					{$i18n.t('Source Files')}
				</div>

				<div class="grid gap-2 md:grid-cols-2">
					{#each sourceFiles as file}
						<div
							class="rounded-xl bg-gray-50 px-3 py-2 font-mono text-xs text-gray-700 dark:bg-gray-850 dark:text-gray-200"
						>
							{file}
						</div>
					{/each}
				</div>
			</section>
		</div>
	</div>
</div>
