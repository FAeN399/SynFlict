<script>
  import '../app.css';
  import { browser } from '$app/environment';
  import { setClient } from 'svelte-apollo';
  import { client } from '$lib/graphql/client';
  
  // Only set the client in the browser to avoid SSR issues
  if (browser) {
    setClient(client);
  }
</script>

<div class="min-h-screen bg-gray-50">
  <slot />
</div>
