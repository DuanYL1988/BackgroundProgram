package com.example.mysql.service;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
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

    @Autowired
    JdbcTemplate jdbcTemplate;

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

        // 一览表示部分
        TableInfoDto condition2 = new TableInfoDto();
        condition2.setTableName(tableName);
        condition2.setColListDisableFlag("1");
        condition.setOrderBy("COL_SORT");
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
                codeList = new ArrayList<Code>();
            }
            codeList.add(code);
            codeMap.put(columns.getCategoryId(),codeList);
        }

        // 名称列表
        String query = "SELECT DISTINCT NAME_CN,NAME,NAME_JP FROM " + tableName + ";";
        List<Code> nameList = jdbcTemplate.query(query, new Object[]{}, new RowMapper<Code>() {
            @Override
            public Code mapRow(ResultSet rs, int rowNum) throws SQLException {
                Code result = new Code();
                result.setCategory("NAME");
                result.setCode(rs.getString("NAME"));
                result.setValue(rs.getString("NAME_CN")+"_"+rs.getString("NAME_JP")+"_"+rs.getString("NAME"));
                return result;
            }
        });
        codeMap.put("NAME",nameList);

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
