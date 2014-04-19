#include <iostream>
#include <stdio.h>
#include <zmq.hpp>
#include <stack>
#include <cmath>
#include <cstring>
#include <string>
#include <vector>
#include <queue>
using namespace std;
const int lambda = 0.5;
const int mu = 0.5;

class form_tree{
private:
	struct node{
		string str;
		int size;
		int depth;
		int label;
		bool terminal;
		vector<int> indexes;
		vector<node *> child;
	}*root;
public:
	form_tree();
	void main_func();
};


node *form_tree::main_func(string str){
	stack<node *> stk;
	node *temp = new node;
	temp.str = str[0];
	temp.child = NULL;
	stk.push(temp);
	string str2 = ""; 

//	(ROOT (SBARQ (WHNP (WP Who)) 
//		(SQ (VP (VBZ needs) (NP (NP (DT a) (NN visa)) (PP (IN for) (NP (NNP Australia)))))) (. ?)))
	
	for(int i=1;i<str.length();i++){
		if(str[i] == ')' || str[i] == '('){
			if(str[i] == ')'){
				vector<node *> children;
				while(!stk.empty()){
					node *temp = stk.top();
					stk.pop();
					if(temp.str == '(')
						break
					else
						children.push_back(temp);
				}
				node *temp3;
				int sz = children.length()-1;
				temp3 -> str = children[sz]->str;
				for(int j=0;j<children.length()-1;j++)
					temp3 -> child.push_back(children[j]);
				temp3->size = 0;
				temp3->label = -1;
				temp3->depth = 0;
				temp3->terminal = false;
				temp3->arr = NULL;
				stk.push(temp3);
			}
			else{
				node *temp2;
				temp2->str = str[i];
				temp2->child = NULL;
				temp2->size = 0;
				temp2->label = -1;
				temp2->depth = 0;
				temp2->terminal = false;
				temp2->arr = NULL;
				stk.push(temp2);
			}
		}
		else{
			if(str[i] != ' ')
				str2 = str2 + str[i];
			else{
				node *temp2;
				temp2.str = str2;
				temp2.child = NULL;
				temp2->size = 0;
				temp2->label = -1;
				temp2->depth = 0;
				temp2->terminal = false;
				temp2->arr = NULL;
				stk.push(temp2);
				str2 = "";
			}
		}
	}
	node *t1 = stk.top();
	return t1;
}

// to assign size and depth for each node

void form_tree::depth(node *t,int dpt){
	if(t -> child.size() == 0)
		return ;
	else{
		t -> depth = dpt;
		dpt++;
		for(int i=0;i<t->child.size();i++)
			depth(t->child[i],dpt);
	}
}

int form_tree::size(node *t){
	if(t -> child.size() == 0)
		return 0;
	else{
		int x = t->child.size();
		for(int i=0;i<t->child.size();i++) 
			x = x + size(t->child[i]);
		return x;
	}
}

void form_tree::size1(node *t){
	for(int i=0;i<t->child.size();i++){
		int sz = size(t->child[i]);
		size1(t->child[i]);
	}
}

void form_tree::level_order(node *t){
	queue<node *> q;
	int idx = 1;
	q.push(t);
	while(!q.empty()){
		node *t1 = q.front();
		q.pop();
		t1->label = idx; 
		if(t1->child.size() == 0)
			t1->terminal = true;
		for(int i=0;i<t1->child.size();i++)
			q.push(t1->child[i]);			
		idx++;
	}	
}

void form_tree::assign_child(node *t){
	for(int i=0;i<t->child.size();i++){
		t->indexes.push_back(t->child[i].label);	
		assign_child(t->child[i]);
	}
}

/*
Main part comes here
calculating M(r1,r2)
*/

int form_tree::total_fragments(node *t){
	queue<node *> q;
	int idx = 0;
	q.push(t);
	while(!q.empty()){
		node *t1 = q.front();
		q.pop();
		for(int i=0;i<t1->child.size();i++)
			q.push(t1->child[i]);			
		idx++;
	}
	return idx;	
}

node *form_tree::get(node *t,int pos){
	queue<node *> q;
	int idx = 0;
	q.push(t);
	while(!q.empty()){
		if(idx == pos)
			return q.front();
		node *t1 = q.front();
		q.pop();
		for(int i=0;i<t1->child.size();i++)
			q.push(t1->child[i]);			
		idx++;
	}	
}

void form_tree::delta(string str){
	if(str == 'VB' || str == 'NN')
		return 1.2;
	else if(str == 'VP' || str == 'NP')
		return 1.1;
	else
		return 1;
}

void form_tree::calculate(node *t1,node *t2){
	int T1 = total_fragments(t1);
	int T2 = total_fragments(t2);
	int eta = 0;
	vector<vector<int> > M(T1,vector<int>(T2,0));
	for(int i=T1-1;i>=0;i--){
		for(int j=T2-1;j>=0;j--){
			//if r1 and r2 are terminals
			node *t3 = get(t1,i);
			node *t4 = get(t2,j);
			if(t3 -> terminal == true && t4 -> terminal == true){
				if(t3 -> str != t4 -> str)
					M[i][j] = 0;
				else{
					eta++;
					M[i][j] = delta(t3->str) * delta(str) * power(lambda,t3->size + t4->size) * power(mu,t3->depth + t4->depth);
				}
			}
			else{
					eta++;
					int r1 = t3 -> child.size();
					int r2 = t4 -> child.size();
					int val = std::min(r1,r2);
					node * temp;
					if(val == r1)
						temp = t3;
					else
						temp = t4;
					int result = 0;
					for(int k=0;k<val;k++)
						result = result * M[t3->child[k]->label][t4->child[k]->label];
					M[i][j] = power(delta(t3->str),eta) * power(delta(t4->str),eta) * power(lambda,2*eta) * /
							  power(mu,eta * (2 -(1 + temp -> child.size())*(t3->depth + t4->depth));

			}
		}
	}
	int main_result = 0;
	for(int i=0;i<M.size();i++){
		for(int j=0;j<M[i].size();j++){
			main_result = main_result + M[i][j];
		}
	}
	return main_result;
}

int main(int argc,char *argv[]){
	depth(t,1);
	t -> size = size(t);
	size1(t);
}