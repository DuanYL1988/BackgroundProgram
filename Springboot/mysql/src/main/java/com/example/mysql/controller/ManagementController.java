package com.example.mysql.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.example.mysql.dto.*;
import com.example.mysql.model.*;
import com.example.mysql.repository.*;
import com.example.mysql.service.ManagementServiceImpl;
import com.example.mysql.service.TableInfoServiceImpl;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ManagementController {

    @Autowired
    TableInfoServiceImpl tableService;

    @Autowired
    FgoServantRepository fgoDao;

    @Autowired
    ArknightsOperatorRepository arknightsDao;

    @Autowired
    WutheringWaveResonatorRepository wutherWaveDao;


    @GetMapping("/getFilterColumns")
    public ResponseResult getFilterColumns(String tableName) {
        Map<String, Object> data = tableService.getList(tableName);
        ResponseResult result = CtrlCommon.success(data);
        return result;
    }

    /**
     * FGO一览检索Contorller
     **/
    @PostMapping("/FGO_SERVANT/getList")
    public ResponseResult getFgoList(@RequestBody FgoServantDto dto) {
        List<FgoServant> resultList = fgoDao.selectByDto(dto);
        Map<String, Object> result = new HashMap<>();
        result.put("dataList",resultList);
        return CtrlCommon.success(result);
    }

    /**
     * 明日方舟一览检索Contorller
     **/
    @PostMapping("/ARKNIGHTS_OPERATOR/getList")
    public ResponseResult getArknightsList(@RequestBody ArknightsOperatorDto dto) {
        List<ArknightsOperator> resultList = arknightsDao.selectByDto(dto);
        Map<String, Object> result = new HashMap<>();
        result.put("dataList",resultList);
        return CtrlCommon.success(result);
    }

    /**
     * FGO一览检索Contorller
     **/
    @PostMapping("/WUTHERING_WAVE_RESONATOR/getList")
    public ResponseResult getwutherWaveList(@RequestBody WutheringWaveResonatorDto dto) {
        List<WutheringWaveResonator> resultList = wutherWaveDao.selectByDto(dto);
        Map<String, Object> result = new HashMap<>();
        result.put("dataList",resultList);
        return CtrlCommon.success(result);
    }

}
