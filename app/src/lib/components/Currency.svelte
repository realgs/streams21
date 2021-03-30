<script>
    import { onMount } from 'svelte'
    import { handleData } from '$lib/services/FinanceApi'

    export let cryptoCurrencyCode
    export let realCurrencyCode

    let downloadedData = []

    $: console.log(downloadedData)

    onMount(() => {
        const interval = setInterval(async () => {
            const data = await handleData(cryptoCurrencyCode, realCurrencyCode)
            downloadedData = [...downloadedData, data]
        }, 5000)

        return () => clearInterval(interval)
    })
</script>

<div>
    <ul>
        {#if downloadedData && downloadedData.length > 0}
            {#each downloadedData as { ask, bid, difference }}
                <li>{ ask } { bid } { difference }</li>
            {/each}
        {/if}
    </ul>
</div>