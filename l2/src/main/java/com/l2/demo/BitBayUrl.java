package com.l2.demo;

import org.springframework.stereotype.Component;
import org.springframework.web.util.UriComponentsBuilder;

@Component
public class BitBayUrl {

    public static final String URL = "https://bitbay.net/API/Public/";

    public static final String URL_SCHEMA = "https";
    public static final String URL_BASE_PATH = "API/Public/";
    public static final String JSON_SUFFIX = ".json";
    public static final String LIMIT = "limit";
    public static final String TYPE = "type";

    public static final String TRADES_NAME = "trades";
    public static final String BUY = "buy";
    public static final String SELL = "sell";


    public static String getUrl(String cryptocurrency, String currency, String type, Integer limit) {
        return UriComponentsBuilder.newInstance()
                .scheme(URL_SCHEMA)
                .host("bitbay.net")
                .path(URL_BASE_PATH)
                .path(cryptocurrency + currency + "/")
                .path(TRADES_NAME + JSON_SUFFIX)
                .queryParam(TYPE, type)
                .queryParam(LIMIT, limit).build()
                .toString();
    }
}
