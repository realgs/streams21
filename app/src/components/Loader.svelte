<script>
  import { onDestroy } from 'svelte';

  export let type = 'slash';
  export let timer = 300;
  export let loading = true;
  export let success = false;
  export let fresh = true;
  export let always_visible = false;
  $: css_class = fresh
    ? ''
    : loading
    ? 'loading'
    : success
    ? 'success'
    : 'fail';

  // Types
  let types = {
    dots: ['.', '..', '...'],
    clock: '◴◷◶◵',
    braille: '⣾⣽⣻⢿⡿⣟⣯⣷',
    squares: '▖▘▝▗',
    slash: '/|\\|',
  };

  let loader;
  let loop;

  let stages = types[type];

  $: if (loading) {
    start();
  } else {
    stop();
  }

  function start() {
    fresh = false;
    let i = 0;
    loader = stages[i];
    loop = setInterval(() => {
      i++;
      if (i == stages.length) {
        i = 0;
      }
      loader = stages[i];
    }, timer);
  }

  function stop() {
    clearInterval(loop);
    loader = always_visible ? '█' : '';
  }

  onDestroy(() => {
    stop();
  });
</script>

<span class={css_class}>{@html loader}</span>
