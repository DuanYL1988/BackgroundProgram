package com.example.sqlite.controller;

import com.example.sqlite.model.Message;

import java.util.List;

public class Response {

    private String code;

    private String message;

    private List<Message> errorList;

    private Object data;

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<Message> getErrorList() {
        return errorList;
    }

    public void setErrorList(List<Message> errorList) {
        this.errorList = errorList;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }
}
