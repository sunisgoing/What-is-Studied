#include "LineTablebyArray.h"
#include "LineTablebyLinklist.h"

//#define TEST_LINETABLE_ARRAY
#define TEST_LINETABLE_LINKLIST

int main(void)
{
#if defined(TEST_LINETABLE_ARRAY)
//test line table by array
  CLineTablebyArray<uint_32>  clta;
  uint_32 i = 0;
  for(i=1;i<=10;i++)
  	clta.Insert(i,100+i);
  cout<<clta.Length()<<endl;
  for(i=1;i<=clta.Length();i++){
  	int tmp = clta.Getdata(i);
  	cout<<tmp<<" ";
  }
  cout<<endl;
  
  clta.Delete(3);
    cout<<clta.Length()<<endl;
  for(i=1;i<=clta.Length();i++){
  	int tmp = clta.Getdata(i);
  	cout<<tmp<<" ";
  }
  cout<<endl;
  
  clta.Clear();
  cout<<clta.Length()<<endl;
  for(i=1;i<=clta.Length();i++){
  	int tmp = clta.Getdata(i);
  	cout<<tmp<<" ";
  }
  cout<<endl;
 
#elif defined(TEST_LINETABLE_LINKLIST) 
//test line table by linklist
  CLineTablebyLinklist<uint_32>  cltb;
  uint_32 i = 0;
  for(i=1;i<=10;i++)
  	cltb.Insert(i,100+i);
  cout<<cltb.Length()<<endl;
  for(i=1;i<=cltb.Length();i++){
  	int tmp = cltb.Getdata(i);
  	cout<<tmp<<" ";
  }
  cout<<endl;
  
  cltb.Delete(3);
    cout<<cltb.Length()<<endl;
  for(i=1;i<=cltb.Length();i++){
  	int tmp = cltb.Getdata(i);
  	cout<<tmp<<" ";
  }
  cout<<endl;
  
  cltb.Clear();
  cout<<cltb.Length()<<endl;
  for(i=1;i<=cltb.Length();i++){
  	int tmp = cltb.Getdata(i);
  	cout<<tmp<<" ";
  }
  cout<<endl;

//test stack

//test queue

//test string

//test matrics

//test tree

//test graph

//test find

//test sort
#endif
	return 0;
}
