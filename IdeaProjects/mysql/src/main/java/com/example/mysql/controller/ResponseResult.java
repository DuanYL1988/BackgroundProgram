package com.example.mysql.controller;

import java.util.List;

import com.example.mysql.model.Message;

import lombok.Data;

@Data
public class ResponseResult {

    private String code;

    private String message;

    private List<Message> errorList;

    private Object data;

}
