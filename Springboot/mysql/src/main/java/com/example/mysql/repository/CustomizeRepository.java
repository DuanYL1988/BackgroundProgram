package com.example.mysql.repository;

import com.example.mysql.dto.CodeMasterDto;
import com.example.mysql.dto.FireemblemHeroDto;
import com.example.mysql.model.CodeMaster;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

/**
 * CODE管理Repository
 */
@Repository
public interface CustomizeRepository {
    /**
     * 查找火纹人物的技能情报
     * @param dto
     * @return
     */
    public List<Map<String, Object>> getFehSkillsInfo(FireemblemHeroDto dto);
}
