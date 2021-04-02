<script>
    import { onMount } from 'svelte'
    import { handleData } from '$lib/services/FinanceApi'
    import Currencyhistory from '$lib/components/CurrencyHistory.svelte'

    export let cryptoCurrencyCode
    export let realCurrencyCode

    let downloadedData = []

    onMount(() => {
        const interval = setInterval(async () => {
            const data = await handleData(cryptoCurrencyCode, realCurrencyCode)
            downloadedData = [...downloadedData, data]
        }, 5000)

        return () => clearInterval(interval)
    })
</script>

<style lang="scss">
</style>

<div>
    <Currencyhistory currencyData="{ downloadedData }" />
</div>