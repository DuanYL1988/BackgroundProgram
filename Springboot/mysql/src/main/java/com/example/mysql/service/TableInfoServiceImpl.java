package com.example.mysql.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.mysql.dto.CodeMasterDto;
import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.CodeMaster;
import com.example.mysql.model.Configration;
import com.example.mysql.model.TableInfo;
import com.example.mysql.repository.CodeMasterRepository;
import com.example.mysql.repository.ConfigrationRepository;
import com.example.mysql.repository.TableInfoRepository;

import lombok.Data;

/**
 * 数据库表管理Service
 */
@Service
public class TableInfoServiceImpl {

    @Autowired
    TableInfoRepository tableinfoRepository;

    @Autowired
    CodeMasterRepository codeRepository;

    @Autowired
    ConfigrationRepository configRepository;

    /**
     * 取得通用的检索信息和列表表示信息
     *
     * @param  dto
     * @return
     */
    public Map<String, Object> getList(String tableName) {
        // 处理结果
        Map<String, Object> result = new HashMap<String, Object>();
        // 检索条件部
        TableInfoDto condition = new TableInfoDto();
        condition.setTableName(tableName);
        condition.setColFifterable("1");
        List<TableInfo> filterColumns = tableinfoRepository.selectByDto(condition);
        result.put("filterColumns", filterColumns);

        // 配置信息
        Configration configInfo = configRepository.selectOneByUniqueKey(tableName);
        result.put("config", configInfo);

        // CODE MAP
        CodeMasterDto codeMasterCond = new CodeMasterDto();
        codeMasterCond.setApplication(tableName);
        List<CodeMaster> codeListResult = codeRepository.selectByDto(codeMasterCond);
        Map<String,List<Code>> codeMap = new HashMap<>();
        for(CodeMaster columns: codeListResult){
            Code code = new Code();
            code.setCategory(columns.getCategoryId());
            code.setCode(columns.getCode());
            code.setValue(columns.getName());
            code.setImgUrl(columns.getImgUrl());
            List<Code> codeList = codeMap.get(columns.getCategoryId());
            if(Objects.isNull(codeList)) {
                codeList = new ArrayList<Code>();
            }
            codeList.add(code);
            codeMap.put(columns.getCategoryId(),codeList);
        }

        result.put("direct", codeMap);
        // 返回结果
        return result;
    }

    @Data
    class Code {
        private String category;
        private String code;
        private String value;
        private String imgUrl;
    }
}
