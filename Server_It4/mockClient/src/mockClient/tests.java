package mockClient;

public class tests {
	public static void main(String[] args){
		tests t = new tests();
		//t.test1();
		//t.test2();
		t.test3();
		//t.test4();
		
	}
	
	public void test1() {
		System.out.print("Test Case 1: ");
		MockClient test1 = new MockClient();
		test1.MockClient(1,"LOCAL","end");
		System.out.println("Test Case 1 END -----");
	}
	
	public void test2() {
		
		System.out.print("Test Case 2: ");
		MockClient test2 = new MockClient();
		test2.MockClient(2,"LOCAL","end");
		System.out.println("Test Case 2 END -----");
	}
	public void test3() {
		System.out.print("Test Case 3: ");
		MockClient test3 = new MockClient();
		test3.MockClient(1,"LOCAL", "C:\\Users\\Jonathan\\Documents\\LED_Globe\\Server_It4\\ReadFileJob1.txt");
		System.out.println("Test Case 3 END -----");
	}
	
	public void test4() {
		System.out.print("Test Case 4: ");
		MockClient test4 = new MockClient();
		test4.MockClient(2,"LOCAL","C:\\Users\\Jonathan\\Documents\\LED_Globe\\Server_It4\\ReadFileJob2.txt");
		System.out.println("Test Case 4 END -----");
	}
}

