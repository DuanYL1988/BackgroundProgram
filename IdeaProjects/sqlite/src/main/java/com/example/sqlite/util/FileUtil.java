package com.example.sqlite.util;

import org.springframework.stereotype.Component;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

@Component
public class FileUtil {

    private static final int FILE_SIZE = 8192;

    /**
     * 字节流输出文件
     *
     * @param ins
     * @param file
     */
    public void inputStreamToFile(InputStream ins, File file) {
        OutputStream out = null;
        try {
            out = new FileOutputStream(file);
            int bytes = 0;
            byte[] buffer = new byte[FILE_SIZE];
            while ((bytes = ins.read(buffer, 0, FILE_SIZE)) != -1) {
                out.write(buffer, 0, bytes);
            }
            out.close();
            ins.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String takeTimestampFileName(String fileTyle) {
        Date currentTime = new Date();
        SimpleDateFormat fmt = new SimpleDateFormat("yyyyMMddHHmmssSSS");
        String result = fmt.format(currentTime);
        return result + "." + fileTyle;
    }

    public static void main(String[] args) {
        String fileName = "aa.png";
        String type = fileName.split("\\.")[1];
        System.out.println(type);
    }
}
