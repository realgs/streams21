<script>
	import CurrencyPlot from '$lib/components/CurrencyPlot.svelte'
</script>

<style lang="scss">
	.container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		height: 100vh;
	}
</style>

<main class="container">
	<CurrencyPlot cryptoCurrencyCode="BTC" realCurrencyCode="USD" />
	<CurrencyPlot cryptoCurrencyCode="ETH" realCurrencyCode="USD" />
	<CurrencyPlot cryptoCurrencyCode="XLM" realCurrencyCode="USD" />
</main>

