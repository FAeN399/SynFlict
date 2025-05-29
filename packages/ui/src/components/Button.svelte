<script lang="ts">
  export let type: 'primary' | 'secondary' | 'danger' | 'ghost' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let disabled = false;
  export let fullWidth = false;
  
  // Compute classes based on props
  $: typeClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    ghost: 'bg-transparent hover:bg-gray-100 text-gray-700'
  }[type];
  
  $: sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3'
  }[size];
  
  $: widthClass = fullWidth ? 'w-full' : '';
  $: disabledClass = disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer';
</script>

<button
  class="rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 {typeClasses} {sizeClasses} {widthClass} {disabledClass}"
  {disabled}
  on:click
>
  <slot />
</button>
