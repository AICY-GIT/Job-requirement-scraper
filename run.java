class Solution {
    public int[] plusOne(int[] digits) {
        for(int i = digits.length-1;i>=0;i--){
            if(digits[i]+1==10){
                digits[i]=0;
            }else{
                digits[i]=digits[i]+1;
                if(i==0){
                    int[] newDigits = new int[digits.length + 1];
                    newDigits[0]=1;
                    for(int j =1;j<newDigits.length;j++){
                        newDigits[j]=digits[j-1];
                    }
                    return newDigits;
                }
                return digits;
            }
        }
        return digits;
    }
}