package com.example.mysql.controller;

import com.example.mysql.model.Message;

import java.util.ArrayList;

public class CtrlCommon {

    public static ResponseResult initResponse(){
        ResponseResult resp = new ResponseResult();
        resp.setCode("200");
        resp.setMessage("SUCCESS");
        resp.setErrorList(new ArrayList<Message>());
        return resp;
    }

    public static ResponseResult success(Object data){
        ResponseResult resp = new ResponseResult();
        resp.setCode("200");
        resp.setMessage("SUCCESS");
        resp.setErrorList(new ArrayList<Message>());
        resp.setData(data);
        return resp;
    }

    public static ResponseResult error(String message){
        ResponseResult resp = new ResponseResult();
        resp.setCode("400");
        resp.setMessage(message);
        resp.setErrorList(new ArrayList<Message>());
        return resp;
    }
}
