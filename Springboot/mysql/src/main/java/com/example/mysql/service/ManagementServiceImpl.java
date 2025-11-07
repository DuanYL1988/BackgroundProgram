package com.example.mysql.service;

import com.example.mysql.dto.BatchColumnDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

@Service
public class ManagementServiceImpl {

    @Autowired
    JdbcTemplate jdbcTemplate;

    public int updateFlagColumn(BatchColumnDto dto){
        String query = "UPDATE " + dto.getTableName() + " SET " + dto.getTgtColNm() + " = CASE " + dto.getCondColNm();
        String[] ids = dto.getIds();
        String[] values = dto.getValues();
        String cond = "";
        for (int i = 0 ; i < ids.length; i++) {
            query += " WHEN '" + ids[i] + "' THEN '" + values[i] + "'";
            cond += "'"+ids[i]+"'";
            if (i<ids.length-1){
                cond += ",";
            }
        }
        query += " ELSE " + dto.getTgtColNm() + " END WHERE " + dto.getCondColNm() + " IN (" + cond + ")";
        System.out.println(query);
        int updateCnt = jdbcTemplate.update(query);
        System.out.println("一共更新了:" + updateCnt);
        return updateCnt;
    }
}
