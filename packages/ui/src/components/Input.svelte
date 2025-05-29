<script lang="ts">
  export let type = 'text';
  export let value = '';
  export let placeholder = '';
  export let label = '';
  export let error = '';
  export let disabled = false;
  export let required = false;
  export let id = '';
  export let name = '';
</script>

<div class="w-full">
  {#if label}
    <label for={id} class="block text-sm font-medium text-gray-700 mb-1">
      {label}{#if required}<span class="text-red-500">*</span>{/if}
    </label>
  {/if}
  
  {#if type === 'text'}
    <input
      {id}
      {name}
      type="text"
      {placeholder}
      {disabled}
      {required}
      bind:value
      class="w-full px-3 py-2 border {error ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      on:input
      on:change
      on:focus
      on:blur
    />
  {:else if type === 'password'}
    <input
      {id}
      {name}
      type="password"
      {placeholder}
      {disabled}
      {required}
      bind:value
      class="w-full px-3 py-2 border {error ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      on:input
      on:change
      on:focus
      on:blur
    />
  {:else if type === 'email'}
    <input
      {id}
      {name}
      type="email"
      {placeholder}
      {disabled}
      {required}
      bind:value
      class="w-full px-3 py-2 border {error ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      on:input
      on:change
      on:focus
      on:blur
    />
  {:else}
    <input
      {id}
      {name}
      type="text"
      {placeholder}
      {disabled}
      {required}
      bind:value
      class="w-full px-3 py-2 border {error ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      on:input
      on:change
      on:focus
      on:blur
    />
  {/if}
  
  {#if error}
    <p class="mt-1 text-sm text-red-600">{error}</p>
  {/if}
</div>
