package com.example.mysql.controller;

import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.TableInfo;
import com.example.mysql.repository.TableInfoRepository;
import com.example.mysql.service.TableInfoServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class SystemController {

    @Autowired
    TableInfoServiceImpl tableInfoService;

    @Autowired
    TableInfoRepository tableDao;

    /**
     * 系统控制-取得表一览
     * @return
     */
    @GetMapping("/systemconf/tableEdit")
    public ResponseResult tableEdit(){
        return CtrlCommon.success(tableInfoService.getTableList());
    }

    @GetMapping("/systemconf/getColumnListByTblnm")
    public ResponseResult getColumnListByTblnm(@RequestParam String tableName){
        TableInfoDto condition = new TableInfoDto();
        condition.setTableName(tableName);
        condition.setOrderBy("COL_SORT");
        List<TableInfo> columnsList = tableDao.selectByDto(condition);
        return CtrlCommon.success(columnsList);
    }
}
