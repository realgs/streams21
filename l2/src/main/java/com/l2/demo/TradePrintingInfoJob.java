package com.l2.demo;

import com.l2.demo.model.CryptoTrade;
import lombok.AllArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
@AllArgsConstructor
public class TradePrintingInfoJob {

    private final BitBayService bitBayService;

    private final List<String> cryptos = Arrays.asList("BTC", "LTC", "DASH");
    public static final String USD = "USD";

    Map<String, List<CryptoTrade>> cryptoPriceBuyLast = new HashMap<>();
    Map<String, List<CryptoTrade>> cryptoPriceSellLast = new HashMap<>();

    @Scheduled(fixedDelay = 5000)
    public void printInfoAboutTrades() {
        updateLastTradeData();

        System.out.println("Crypto to buy:");
        for (String crypto : cryptoPriceBuyLast.keySet()) {
            System.out.println(crypto + bitBayService.getCryptoTradeBuy(crypto, USD));
        }

        System.out.println("Crypto to sell:");
        for (String crypto : cryptoPriceSellLast.keySet()) {
            System.out.println(crypto + bitBayService.getCryptoTradeSell(crypto, USD));
        }

        System.out.println("Crypto difference(1 - (price sell - price buy) / price buy)):");
        for (String crypto :
                cryptos) {
            double sumBuy = cryptoPriceBuyLast.get(crypto).stream().mapToDouble(CryptoTrade::getPrice).sum();
            double sumSell = cryptoPriceSellLast.get(crypto).stream().mapToDouble(CryptoTrade::getPrice).sum();
            double rating = 1.0 - (sumSell - sumBuy) / sumBuy;
            System.out.println(crypto + " : " + rating);
        }
    }

    private void updateLastTradeData() {
        for (String crypto : cryptos) {
            cryptoPriceBuyLast.put(crypto, bitBayService.getCryptoTradeBuy(crypto, USD));
        }
        for (String crypto : cryptos) {
            cryptoPriceSellLast.put(crypto, bitBayService.getCryptoTradeSell(crypto, USD));
        }
    }
}
