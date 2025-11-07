package com.example.mysql.controller;

import com.example.mysql.service.TableInfoServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SystemController {

    @Autowired
    TableInfoServiceImpl tableInfoService;

    /**
     * 系统控制-取得表一览
     * @return
     */
    @GetMapping("/systemconf/tableEdit")
    public ResponseResult tableEdit(){
        return CtrlCommon.success(tableInfoService.getTableList());
    }
}
