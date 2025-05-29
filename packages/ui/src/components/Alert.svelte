<script lang="ts">
  export let type: 'info' | 'success' | 'warning' | 'error' = 'info';
  export let dismissible = false;
  
  let visible = true;
  
  // Compute classes based on props
  $: typeClasses = {
    info: 'bg-blue-50 text-blue-800 border-blue-200',
    success: 'bg-green-50 text-green-800 border-green-200',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
    error: 'bg-red-50 text-red-800 border-red-200'
  }[type];
  
  $: iconType = {
    info: '💡',
    success: '✅',
    warning: '⚠️',
    error: '❌'
  }[type];
  
  function dismiss() {
    visible = false;
  }
</script>

{#if visible}
  <div class="rounded-md border p-4 {typeClasses}">
    <div class="flex">
      <div class="flex-shrink-0 mr-3">
        {iconType}
      </div>
      <div class="flex-1">
        <slot />
      </div>
      {#if dismissible}
        <div class="ml-auto pl-3">
          <button 
            type="button" 
            class="inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            on:click={dismiss}
          >
            <span class="sr-only">Dismiss</span>
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      {/if}
    </div>
  </div>
{/if}
