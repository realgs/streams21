<script>
    export let currencyData
</script>

<style lang="scss">
    .table-history {
        position: relative;
        &__header, &__body {
            &--row {
                height: 30px;
                display: flex;
                flex-direction: row;
            }

            &--cell {
                width: 80px;
            }
        }

        &__body {
            padding-top: 30px;
            position: absolute;

            &--scroll {
                display: flex;
                flex-direction: column;
                overflow-y: auto;
                max-height: 90px;
            }
        }
    }
</style>

<div class="table-history">
    {#if currencyData && currencyData.length > 0}
    <div class="table-history__header"></div>
        <div class="table-history__header--row">
            <div class="table-history__header--cell"><span>ask</span></div>
            <div class="table-history__header--cell"><span>bid</span></div>
            <div class="table-history__header--cell"><span>difference</span></div>
        </div>
    <div class="table-history__body">
        <div class="table-history__body--scroll">
            {#each currencyData as { ask, bid, difference}}
            <div class="table-history__body--row">
                <div class="table-history__body--cell"><span>{ ask }</span></div>
                <div class="table-history__body--cell"><span>{ bid }</span></div>
                <div class="table-history__body--cell"><span>{ difference } %</span></div>
            </div>
            {/each}
        </div>
    </div>
    {/if}
</div>