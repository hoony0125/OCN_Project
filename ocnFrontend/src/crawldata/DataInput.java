
package crawldata;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import db.DBConnection;
import db.Insert;

public class DataInput {

	public static void main(String[] args) 
	{	
		DBConnection.initConnecton();
		
		List<List<String>> list = null;
		
		DataInput reader = new DataInput();
		list = reader.getCSV();
		
		for(int i = 0; i < list.size(); i++)
		{
			for(int j = 0; j < 3; j++)
			{
				list.get(i).set( j , list.get(i).get(j).replace("^+^","\""));
				list.get(i).set( j , list.get(i).get(j).replace("^",","));
			}	
		}
		
		System.out.println(list.size());
		Insert it = new Insert();
		
		for( int i = 0; i < list.size(); i++)
		{
			String ATITLE = list.get(i).get(0);
			String AUPLOAD = list.get(i).get(1);
			String ACONTENT = list.get(i).get(2);
			String AREGDATE = "SYSDATE";
			String APRESSCOM = list.get(i).get(4);
			String AFILENAME = list.get(i).get(3);
			int ACATEGORY = Integer.parseInt(list.get(i).get(5));
			
			boolean result = it.insert(ATITLE, AUPLOAD, ACONTENT, AREGDATE, APRESSCOM, AFILENAME , ACATEGORY);
			if(result)
			{
				System.out.println( i + " : 정상적으로 추가되었습니다");
			}
		}
		
	}
	
	public List<List<String>> getCSV()
	{
		
		List<List<String>> csvList = new ArrayList<List<String>>();
		
		File csv = new File("C:\\Users\\kkh87\\Desktop\\멀캠 파이널 3조\\크롤링관련\\BBC1202.csv");       // 절대 경로 변경
		System.out.println(csv.exists());
		
		BufferedReader br = null;
		String line = "";
		
        try
        {
            br = new BufferedReader(new FileReader(csv));
            while ((line = br.readLine()) != null) 
            { 

                List<String> aLine = new ArrayList<String>();
                String[] lineArr = line.split(",", -1); 
                

                aLine = Arrays.asList(lineArr);
                csvList.add(aLine);
            }
        } 
        catch (FileNotFoundException e) 
        {
            e.printStackTrace();
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        } 
        finally 
        {
            try 
            {
                if (br != null) 
                { 
                    br.close();
                }
            }
            catch(IOException e) 
            {
                e.printStackTrace();
            }
        }
        return csvList;
	}
	
}




