package com.example.mysql.controller;

import com.example.mysql.dto.FireemblemHeroDto;
import com.example.mysql.service.FehServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FehController {

    @Autowired
    FehServiceImpl fehService;

    /**
     * 数据管理火纹一览检索Contorller
     **/
    @PostMapping("/FIREEMBLEM_HERO/getList")
    public ResponseResult getFehManageList(@RequestBody FireemblemHeroDto dto) {
        return CtrlCommon.success(fehService.getHerosInfo(dto));
    }

}
