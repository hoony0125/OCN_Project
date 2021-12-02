package db;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

public class Insert 
{
	
	public boolean insert(String ATITLE, String AUPLOAD, String ACONTENT, String AREGDATE, String APRESSCOM, String AFILENAME ,int ACATEGORY) 
	{	
		
		String sql = " INSERT INTO ARTICLE(ATITLE, AUPLOAD, ACONTENT, AREGDATE, APRESSCOM, AFILENAME ,AREADCOUNT, ACATEGORY) "   
				+ " VALUES(?, ?, ?, ?, ?, ?, 0, ?) ";  
		Connection conn = null; 
		PreparedStatement psmt = null;
		
		int count = 0;
		
		try
		{
			conn = DBConnection.getConnection();
			
			psmt = conn.prepareStatement(sql);
			psmt.setString(1,  ATITLE);
			psmt.setString(2,  AUPLOAD);
			psmt.setString(3,  ACONTENT);
			psmt.setString(4,  AREGDATE);
			psmt.setString(5,  APRESSCOM);
			psmt.setString(6,  AFILENAME);
			psmt.setInt(7,  ACATEGORY);
			
			count = psmt.executeUpdate();

			
		}catch (SQLException e) {
			e.printStackTrace();
			System.out.println("addArticle fail");
		}finally {
			DBClose.close(conn, psmt, null);
		}
		
		if(count > 0)
			return true;
		return false;

	}
	
}


