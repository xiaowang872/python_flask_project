// import java.util.Scanner;

// public class Main {
//     /**
//      * 返回在指定年薪、房价、房价增长率、年限条件下，程序员买得起房的年份。
//      *
//      * @param salary 指定年薪。
//      * @param price  指定房价。
//      * @param rate   指定房价增长率。
//      * @param year   指定年限。
//      * @return 程序员买得起房的年份；如果始终买不起则为-1。
//      */
//     public int affordHomePrice(int salary, int price, int rate, int year) {
//         int savings = salary; // 当前积蓄，初始为指定年薪salary
//         double homePrice = price; // 当前房价，初始为指定房价price
//         /* 从第一年依次遍历到第year年 */
//         for (int i = 1; i <= year; i++) {
//             if (savings >= homePrice) { // 如果当前积蓄savings大于等于当前房价homePrice
//                 return i; // 说明当前年份i买得起房，返回当前年份i
//             }
//             savings += salary; // 增加积蓄
//             homePrice *= (1 + rate / 100.0); // 房价上涨
//         }
//         return -1; // 指定year年限内始终买不起房，返回-1
//     }

//     public static void main(String[] args) {
//         Scanner input = new Scanner(System.in);
//         Main call = new Main();
//         int N = input.nextInt();
//         int K = input.nextInt();
//         int ans = call.affordHomePrice(N, 200, K, 20);
//         System.out.print(ans == -1 ? "Impossible" : ans);
        
//         input.close(); // 关闭Scanner，释放资源
//     }
// }
    
