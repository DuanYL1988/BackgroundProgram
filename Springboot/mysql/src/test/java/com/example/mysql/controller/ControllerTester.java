package com.example.mysql.controller;

import com.example.mysql.dto.AccountDto;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import java.nio.charset.Charset;
import java.util.Map;

@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class ControllerTester {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    private String token = "";

    @Before
    public void init() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"admin\",\"password\":\"1\"}"))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        String responseContent = result.getResponse().getContentAsString(Charset.forName("UTF-8"));

        ResponseResult response = objectMapper.readValue(responseContent,ResponseResult.class);
        Map<String, String> resultMap = (Map<String, String>) response.getData();
        token = resultMap.get("token");
    }

    @Test
    public void test() throws Exception {
        System.out.println("token:"+token);
    }

    /**
     * 表名取得情报Controller
     */
    @Test
    public void ManagementControllerTest() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/getFilterColumns?tableName=FIREEMBLEM_HERO")
                .header("Authorization", token))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        String responseContent = result.getResponse().getContentAsString(Charset.forName("UTF-8"));
        System.out.println("响应内容：" + responseContent);
    }

    @Test
    public void getFehListTest() throws Exception {
        String json = "{\"nameCn\":\"琳\"}";
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.post("/fireemblem/getList")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json)
                .header("Authorization", token))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        String responseContent = result.getResponse().getContentAsString(Charset.forName("UTF-8"));
        System.out.println("响应内容：" + responseContent);
    }

    @Test
    public void testGetColumns() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/systemconf/getColumnListByTblnm?tableName=FIREEMBLEM_HERO")
                .header("Authorization", token))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();
        String responseContent = result.getResponse().getContentAsString(Charset.forName("UTF-8"));
        System.out.println("响应内容：" + responseContent);
    }
}
