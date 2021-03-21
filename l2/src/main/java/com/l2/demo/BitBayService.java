package com.l2.demo;

import com.l2.demo.model.CryptoTrade;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import static com.l2.demo.BitBayUrl.BUY;
import static com.l2.demo.BitBayUrl.SELL;

@Service
public class BitBayService {

    private final RestTemplate restTemplate = new RestTemplate();

    public List<CryptoTrade> getCryptoTrade(String cryptocurrency, String currency, String type, Integer limit) {
        CryptoTrade[] cryptoTrades = restTemplate.getForObject(BitBayUrl.getUrl(cryptocurrency, currency, type, limit), CryptoTrade[].class);
        return Arrays.stream(cryptoTrades)
                .filter(cryptoTrade -> cryptoTrade.getType().equals(type))
                .limit(limit)
                .collect(Collectors.toList());
    }

    public List<CryptoTrade> getCryptoTradeSell(String cryptocurrency, String currency) {
        return getCryptoTrade(cryptocurrency, currency, SELL, 50);
    }


    public List<CryptoTrade> getCryptoTradeBuy(String cryptocurrency, String currency) {
        return getCryptoTrade(cryptocurrency, currency, BUY, 50);
    }


}
