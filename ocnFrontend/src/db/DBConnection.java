package db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection 
{
	public static void initConnecton()
	{
		try 
		{
			Class.forName("com.mysql.cj.jdbc.Driver");
			System.out.println("Driver Loading Success!");
		}
		catch (ClassNotFoundException e) 
		{
			e.printStackTrace();
		}
	}
	
	public static Connection getConnection()
	{
		Connection conn = null;    // Connection 타입 확인
		try {
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/ocn_db", "root", "mysql");
			// System.out.println("DB Connection Success!");
		} catch (SQLException e) 
		{
			e.printStackTrace();
		} 
		return conn;
	}

}





