<script lang="ts">
  import { Button, Card, Input, Alert } from '@synflict/ui';
  import { query } from 'svelte-apollo';
  import { HELLO_QUERY, GET_USERS } from '$lib/graphql/queries';

  // Demo GraphQL queries
  const hello = query(HELLO_QUERY);
  const users = query(GET_USERS);

  let inputValue = '';
  let alertVisible = true;
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 py-12 px-4">
  <div class="max-w-3xl mx-auto">
    <!-- Hero Section -->
    <Card padding="lg" shadow="lg" rounded="lg" border={true} class="mb-10">
      <h1 class="text-4xl font-bold text-blue-700 mb-2">SynFlict Demo</h1>
      <p class="text-lg text-gray-700 mb-4">A showcase of UI components and GraphQL integration in a modern Turborepo monorepo.</p>
      <div class="flex flex-wrap gap-3 mb-3">
        <a href="/" class="inline-block"><Button type="primary">Home</Button></a>
        <a href="/users" class="inline-block"><Button type="secondary">User Management</Button></a>
        <a href="/docs" class="inline-block"><Button type="ghost">Docs</Button></a>
      </div>
      <div class="text-sm text-gray-500">Monorepo: SvelteKit + Fastify + GraphQL + Tailwind + pnpm + Turbo</div>
    </Card>

    <!-- UI Component Demos -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
      <Card padding="md" shadow="md" rounded="md" border={true}>
        <h2 class="text-xl font-semibold mb-4">Buttons</h2>
        <div class="flex flex-wrap gap-3">
          <Button type="primary">Primary</Button>
          <Button type="secondary">Secondary</Button>
          <Button type="danger">Danger</Button>
          <Button type="ghost">Ghost</Button>
          <Button type="primary" disabled={true}>Disabled</Button>
        </div>
      </Card>
      <Card padding="md" shadow="md" rounded="md" border={true}>
        <h2 class="text-xl font-semibold mb-4">Input</h2>
        <Input label="Demo Input" placeholder="Type something..." bind:value={inputValue} />
        <div class="mt-2 text-sm text-gray-500">Value: <span class="font-mono">{inputValue}</span></div>
      </Card>
      <Card padding="md" shadow="md" rounded="md" border={true}>
        <h2 class="text-xl font-semibold mb-4">Alerts</h2>
        {#if alertVisible}
          <Alert type="info" dismissible={true} on:dismiss={() => alertVisible = false}>
            This is an info alert. Dismiss me!
          </Alert>
        {:else}
          <Button type="ghost" on:click={() => alertVisible = true}>Show Alert Again</Button>
        {/if}
        <Alert type="success" class="mt-3">Success Alert Example</Alert>
        <Alert type="warning" class="mt-3">Warning Alert Example</Alert>
        <Alert type="error" class="mt-3">Error Alert Example</Alert>
      </Card>
      <Card padding="md" shadow="md" rounded="md" border={true}>
        <h2 class="text-xl font-semibold mb-4">Cards</h2>
        <Card padding="sm" shadow="sm" rounded="sm" border={true}>
          <div class="text-sm">This is a nested Card component!</div>
        </Card>
      </Card>
    </div>

    <!-- GraphQL API Demos -->
    <Card padding="lg" shadow="md" rounded="md" border={true} class="mb-10">
      <h2 class="text-2xl font-semibold mb-4">GraphQL API Demo</h2>
      <div class="mb-4">
        <div class="font-mono text-sm text-gray-500 mb-1">Query: hello</div>
        {#if $hello.loading}
          <div class="text-blue-500">Loading...</div>
        {:else if $hello.error}
          <Alert type="error">Error: {$hello.error.message}</Alert>
        {:else}
          <Alert type="success">API says: <span class="font-mono">{$hello.data.hello}</span></Alert>
        {/if}
      </div>
      <div>
        <div class="font-mono text-sm text-gray-500 mb-1">Query: users</div>
        {#if $users.loading}
          <div class="text-blue-500">Loading users...</div>
        {:else if $users.error}
          <Alert type="error">Error: {$users.error.message}</Alert>
        {:else}
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-2 text-left">Name</th>
                  <th class="px-4 py-2 text-left">Email</th>
                  <th class="px-4 py-2 text-left">Role</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-100">
                {#each $users.data.users as user (user.id)}
                  <tr>
                    <td class="px-4 py-2">{user.name}</td>
                    <td class="px-4 py-2">{user.email}</td>
                    <td class="px-4 py-2">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'}">
                        {user.role}
                      </span>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/if}
      </div>
    </Card>

    <!-- Footer -->
    <div class="text-center text-gray-400 text-xs mt-6">
      SynFlict Turborepo Demo &copy; {new Date().getFullYear()}
    </div>
  </div>
</div>
