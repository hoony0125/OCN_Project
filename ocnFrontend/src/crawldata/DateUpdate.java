package crawldata;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import db.DBClose;
import db.DBConnection;
import db.StringProcess;
// DataInput.java 실행 시키고 난 후에 DateUpdate도 실행시켜줄 것 
public class DateUpdate 
{	
	public static void main(String[] args) 
	{	
		
		DateUpdate process = new DateUpdate();
		int allCount = process.searchallNum();
		
		for(int i = 1; i <= allCount; i++)
		{
			process.Search(i);
		}
	}

	public void Update(int seq, String aupload) 
	{	
		String sql = " UPDATE ARTICLE "
				+ "     SET AUPLOAD = ? "
				+ "     WHERE SEQ = ? ";
		
		Connection conn = DBConnection.getConnection();
		PreparedStatement psmt = null;
		int count = 0;
		
		try 
		{		
			conn = DBConnection.getConnection();

			psmt = conn.prepareStatement(sql);
			psmt.setString(1,  aupload);
			psmt.setInt(2,  seq);
					
			count = psmt.executeUpdate();
			
		}catch (SQLException e) 
		{			
			e.printStackTrace();
		} 
		finally 
		{
			DBClose.close(conn, psmt, null);
		}

		if(count > 0) {
			System.out.println(seq + " : 날짜 변화 진행 성공");
		}else{
			System.out.println(seq + " : 날짜 변화 진행 실패");
		}
	}

	public void Search(int seq)
	{
		String sql = " SELECT * " 
				+ "FROM ARTICLE "
				+ "WHERE SEQ = ? ";
		
		Connection conn = DBConnection.getConnection();
		PreparedStatement psmt = null;
		ResultSet rs = null;
		
		try 
		{
			psmt = conn.prepareStatement(sql);
			psmt.setInt(1,  seq);   
			rs = psmt.executeQuery();
			
			if(rs.next() == true)     
			{
				String aupload = rs.getString("aupload");   	
				
				if(aupload.contains("November") || aupload.contains("December"))
				{
					StringProcess func = new StringProcess();
					aupload = func.strProcess(aupload);
					Update(seq, aupload); 
				}
				else
					System.out.println(seq + " : 날짜 변화 없음");
			}
			
		} catch (SQLException e) 
		{
			e.printStackTrace();
		}
		finally
		{
			DBClose.close(conn, psmt, rs);
		}
	}
	
	public int searchallNum()
	{
		String sql = " SELECT COUNT(*) " 
				+ "FROM ARTICLE ";
		
		Connection conn = DBConnection.getConnection();
		PreparedStatement psmt = null;
		ResultSet rs = null;
		
		int allCount = 0;
		try 
		{
			psmt = conn.prepareStatement(sql);   
			rs = psmt.executeQuery();
			
			if(rs.next() == true)     
			{
				allCount = rs.getInt("count(*)");   	
			}
			
		} catch (SQLException e) 
		{
			e.printStackTrace();
		}
		finally
		{
			DBClose.close(conn, psmt, rs);
		}
		return allCount;
	}

}