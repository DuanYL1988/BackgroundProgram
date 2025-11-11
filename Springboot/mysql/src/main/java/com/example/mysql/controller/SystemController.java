package com.example.mysql.controller;

import com.example.mysql.dto.BatchColumnDto;
import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.TableInfo;
import com.example.mysql.repository.TableInfoRepository;
import com.example.mysql.service.ManagementServiceImpl;
import com.example.mysql.service.TableInfoServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class SystemController {

    @Autowired
    TableInfoServiceImpl tableInfoService;

    @Autowired
    TableInfoRepository tableDao;

    @Autowired
    ManagementServiceImpl managementService;
    /**
     * 系统控制-取得表一览
     * @return
     */
    @GetMapping("/systemconf/tableEdit")
    public ResponseResult tableEdit(){
        return CtrlCommon.success(tableInfoService.getTableList());
    }

    @PostMapping("/systemconf/getColumnListByTblnm")
    public ResponseResult getColumnListByTblnm(@RequestBody TableInfoDto condition){
        List<TableInfo> columnsList = tableDao.selectByDto(condition);
        return CtrlCommon.success(columnsList);
    }

    @PostMapping("/systemconf/updateColumnValues")
    public ResponseResult updateColumnValues(@RequestBody BatchColumnDto dto) {
        // TODO
        int updateCnt = managementService.updateFlagColumn(dto);
        ResponseResult result = CtrlCommon.success(dto);
        result.setMessage("Table:" + dto.getTableName()+ "批量更新成功,更新了"+updateCnt+"条数据!");
        return result;
    }
}
