<script lang="ts">
  export let padding: 'sm' | 'md' | 'lg' = 'md';
  export let shadow: 'none' | 'sm' | 'md' | 'lg' = 'md';
  export let rounded: 'none' | 'sm' | 'md' | 'lg' = 'md';
  export let border = false;
  
  // Compute classes based on props
  $: paddingClasses = {
    sm: 'p-2',
    md: 'p-4',
    lg: 'p-6'
  }[padding];
  
  $: shadowClasses = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow',
    lg: 'shadow-lg'
  }[shadow];
  
  $: roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg'
  }[rounded];
  
  $: borderClass = border ? 'border border-gray-200' : '';
</script>

<div class="bg-white {paddingClasses} {shadowClasses} {roundedClasses} {borderClass}">
  <slot />
</div>
