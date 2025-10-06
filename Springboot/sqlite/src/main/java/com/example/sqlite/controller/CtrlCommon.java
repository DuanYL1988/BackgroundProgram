package com.example.sqlite.controller;

import com.example.sqlite.model.Message;

import java.util.ArrayList;

public class CtrlCommon {

    public static Response initResponse(){
        Response resp = new Response();
        resp.setCode("200");
        resp.setMessage("SUCCESS");
        resp.setErrorList(new ArrayList<Message>());
        return resp;
    }

    public static Response success(Object data){
        Response resp = new Response();
        resp.setCode("200");
        resp.setMessage("SUCCESS");
        resp.setErrorList(new ArrayList<Message>());
        resp.setData(data);
        return resp;
    }

    public static Response error(String message){
        Response resp = new Response();
        resp.setCode("400");
        resp.setMessage(message);
        resp.setErrorList(new ArrayList<Message>());
        return resp;
    }
}
