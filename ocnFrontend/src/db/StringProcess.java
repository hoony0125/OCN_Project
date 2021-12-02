package db;

public class StringProcess 
{
	public String strProcess(String aupload) 
	{				

		String in_str = aupload;
		String year = "";
		String month = "";
		String day = "";
		String result = in_str;

		boolean replace = false;
		int split = 0;
		
		if(in_str.contains("November"))
		{	
			in_str = in_str.replace("November", "");
			replace = true;
			month = "11";
		}
		else if(in_str.contains("December"))
		{
			in_str = in_str.replace("December", "");
			replace = true;
			month = "12";
		}	
		
		if(replace)
		{
			String[] array = in_str.split(",");
			for(int i=0; i< array.length; i++) 
			{
				array[i] = array[i].trim();
				if(array[i].length() == 4){
					year = array[i];
					split++;
				}
				else if(array[i].length() == 2 || array[i].length() == 1){
					day = array[i];
					split++;
				}
				if(split == 2) {
					result = year + "-" + month + "-" + day;
				}
				
			}
		}
		
		return result;
	}			
}