package com.example.mysql.service;

import com.example.mysql.dto.CodeMasterDto;
import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.CodeMaster;
import com.example.mysql.model.Configration;
import com.example.mysql.model.TableInfo;
import com.example.mysql.repository.CodeMasterRepository;
import com.example.mysql.repository.ConfigrationRepository;
import com.example.mysql.repository.TableInfoRepository;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

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

    @Autowired
    JdbcTemplate jdbcTemplate;

    /**
     * 取得通用的检索信息和列表表示信息
     */
    public Map<String, Object> getList(String tableName) {
        // 处理结果
        Map<String, Object> result = new HashMap<>();
        // 检索条件部
        TableInfoDto condition = new TableInfoDto();
        condition.setTableName(tableName);
        condition.setColFifterable("1");
        condition.setOrderBy("COL_SORT");
        List<TableInfo> filterColumns = tableinfoRepository.selectByDto(condition);
        result.put("filterColumns", filterColumns);

        // 一览表示部分
        TableInfoDto condition2 = new TableInfoDto();
        condition2.setTableName(tableName);
        condition2.setColListDisableFlag("1");
        condition2.setOrderBy("COL_SORT");
        List<TableInfo> listColumns = tableinfoRepository.selectByDto(condition2);
        result.put("listColumns", listColumns);

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
                codeList = new ArrayList<>();
            }
            codeList.add(code);
            codeMap.put(columns.getCategoryId(),codeList);
        }

        // 名称列表
        String query = "SELECT DISTINCT NAME_CN,NAME,NAME_JP FROM " + tableName + ";";
        List<Code> nameList = jdbcTemplate.query(query, (rs, rowNum) -> {
            Code result1 = new Code();
            result1.setCategory("NAME");
            result1.setCode(rs.getString("NAME"));
            result1.setValue(rs.getString("NAME_CN")+"_"+rs.getString("NAME_JP")+"_"+rs.getString("NAME"));
            return result1;
        });
        codeMap.put("NAME",nameList);
        result.put("direct", codeMap);
        // 返回结果
        return result;
    }

    /**
     * 取得表信息中的所有表名
     */
    public Map<String, Object> getTableList(){
        String query = "SELECT TBL1.TABLE_NAME, MST.NAME FROM (" +
                "SELECT DISTINCT TABLE_NAME FROM TABLE_INFO) TBL1 LEFT JOIN CODE_MASTER mst " +
                "ON TBL1.TABLE_NAME = mst.CODE AND mst.CATEGORY_ID = 'TABLE_NAME'";
        List<Code> tableList = jdbcTemplate.query(query, (rs, rowNum) -> {
            Code result = new Code();
            result.setCode(rs.getString("TABLE_NAME"));
            result.setValue(rs.getString("NAME"));
            return result;
        });
        // 处理结果
        Map<String, Object> result = new HashMap<>();
        result.put("tableList",tableList);
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
