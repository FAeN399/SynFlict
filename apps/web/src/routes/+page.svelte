<script>
  import { Button, Card, Alert } from '@synflict/ui';
  import { query } from 'svelte-apollo';
  import { HELLO_QUERY } from '$lib/graphql/queries';
  
  // Query to fetch the hello message from the GraphQL API
  const hello = query(HELLO_QUERY);
</script>

<div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
  <Card padding="lg" shadow="lg" rounded="lg" border={true} class="max-w-2xl w-full">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-blue-600 mb-6">Welcome to SynFlict</h1>
      <p class="text-xl text-gray-700 mb-8">A modern full-stack application built with Turborepo, SvelteKit, and GraphQL</p>
      
      {#if $hello.loading}
        <div class="flex justify-center items-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      {:else if $hello.error}
        <Alert type="error" dismissible={true}>
          Error connecting to GraphQL API: {$hello.error.message}
        </Alert>
      {:else}
        <Alert type="success" dismissible={false}>
          <p class="font-medium">API Connection Successful!</p>
          <p>Message from API: "{$hello.data.hello}"</p>
        </Alert>
      {/if}
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <a href="/users" class="block">
          <Card padding="md" shadow="md" rounded="md" border={true} class="h-full hover:shadow-lg transition-shadow duration-200">
            <div class="flex flex-col items-center p-4">
              <h2 class="text-xl font-semibold text-gray-800 mb-2">User Management</h2>
              <p class="text-gray-600 text-center mb-4">View and manage users from the GraphQL API</p>
              <Button type="primary">View Users</Button>
            </div>
          </Card>
        </a>
        
        <a href="https://github.com/" target="_blank" rel="noopener noreferrer" class="block">
          <Card padding="md" shadow="md" rounded="md" border={true} class="h-full hover:shadow-lg transition-shadow duration-200">
            <div class="flex flex-col items-center p-4">
              <h2 class="text-xl font-semibold text-gray-800 mb-2">Project Repository</h2>
              <p class="text-gray-600 text-center mb-4">View the source code and documentation</p>
              <Button type="secondary">View on GitHub</Button>
            </div>
          </Card>
        </a>
      </div>
      
      <div class="mt-8 border-t pt-6">
        <p class="text-sm text-gray-500">
          Built with <a href="https://turbo.build/" class="text-blue-500 hover:text-blue-700 underline">Turborepo</a>, 
          <a href="https://kit.svelte.dev/" class="text-blue-500 hover:text-blue-700 underline">SvelteKit</a>, 
          <a href="https://tailwindcss.com/" class="text-blue-500 hover:text-blue-700 underline">Tailwind CSS</a>, and 
          <a href="https://the-guild.dev/graphql/yoga-server" class="text-blue-500 hover:text-blue-700 underline">GraphQL Yoga</a>
        </p>
      </div>
    </div>
  </Card>
</div>
