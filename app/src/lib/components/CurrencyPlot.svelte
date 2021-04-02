<script>
    import { onMount } from 'svelte'
    import { handleData } from '$lib/services/FinanceApi'

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
    .wrapper {
        width: 33.33%;
        margin: 0 auto;
    }

    .currency-table {
        width: 100%;
        position: relative;
        display: inline-block;

        th, td {
            max-width: 33.33%;
            text-align: left;
        }

        thead, tbody {
            width: 100%;
        }

        &__body {
            overflow: auto;
            max-height: 150px;
        }
    }
</style>

<div class="wrapper">
    {#if downloadedData && downloadedData.length > 0}
    <table class="currency-table">
        <thead>
            <tr>
                <th>Ask</th>
                <th>Bid</th>
                <th>Difference</th>
            </tr>
        </thead>
        <div class="currency-table__body">
            <tbody>
                    {#each downloadedData as { ask, bid, difference }}
                    <tr>
                        <td>{ ask } </td>
                        <td>{ bid } </td>
                        <td>{ difference } </td>
                    </tr>
                    {/each}
            </tbody>
        </div>
    </table>
    {/if}
</div>