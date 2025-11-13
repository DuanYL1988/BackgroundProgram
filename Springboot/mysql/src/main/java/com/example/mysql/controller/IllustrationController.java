package com.example.mysql.controller;

import com.example.mysql.dto.FireemblemHeroDto;
import com.example.mysql.service.IllustrationServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class IllustrationController {

    @Autowired
    IllustrationServiceImpl illustrationService;

    /**
     * 火纹一览检索Contorller
     **/
    @PostMapping("/Illustration/FIREEMBLEM_HERO")
    public ResponseResult getFehList(@RequestBody FireemblemHeroDto dto) {
        ResponseResult result = CtrlCommon.success(illustrationService.getHerosInfo(dto));
        return result;
    }

}
