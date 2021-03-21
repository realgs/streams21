package com.l2.demo.model;

import lombok.Data;

@Data
public class CryptoTrade {

    private Integer date;
    private Double price;
    private String type;
    private Double amount;
    private String tid;
}
