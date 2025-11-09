package com.example.mysql.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.example.mysql.dto.BatchColumnDto;
import com.example.mysql.dto.FgoServantDto;
import com.example.mysql.dto.FireemblemHeroDto;
import com.example.mysql.model.FgoServant;
import com.example.mysql.model.FireemblemHero;
import com.example.mysql.repository.FgoServantRepository;
import com.example.mysql.repository.FireemblemHeroRepository;
import com.example.mysql.service.ManagementServiceImpl;
import com.example.mysql.service.TableInfoServiceImpl;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.example.mysql.model.CodeMaster;
import com.example.mysql.model.TableInfo;
import com.example.mysql.repository.CodeMasterRepository;
import com.example.mysql.repository.TableInfoRepository;

@RestController
public class ManagementController {

    @Autowired
    TableInfoServiceImpl tableService;

    @Autowired
    FireemblemHeroRepository fehDao;

    @Autowired
    FgoServantRepository fgoDao;

    @GetMapping("/getFilterColumns")
    public ResponseResult getFilterColumns(String tableName) {
        Map<String, Object> data = tableService.getList(tableName);
        ResponseResult result = CtrlCommon.success(data);
        return result;
    }

    /**
     * 火纹一览检索Contorller
     **/
    @PostMapping("/FIREEMBLEM_HERO/getList")
    public ResponseResult getFehList(@RequestBody FireemblemHeroDto dto) {
        List<FireemblemHero> resultList = fehDao.selectByDto(dto);
        ResponseResult result = CtrlCommon.success(resultList);
        return result;
    }

    /**
     * FGO一览检索Contorller
     **/
    @PostMapping("/FGO_SERVANT/getList")
    public ResponseResult getFgoList(@RequestBody FgoServantDto dto) {
        List<FgoServant> resultList = fgoDao.selectByDto(dto);
        ResponseResult result = CtrlCommon.success(resultList);
        return result;
    }

}
