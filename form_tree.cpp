#include <iostream>
#include <stdio.h>
#include <zmq.hpp>
#include <stack>
#include <cmath>
#include <cstring>
#include <string>
#include <vector>
#include <sstream>
#include <queue>
using namespace std;
const int lambda = 0.5;
const int mu = 0.5;

struct node{
	string str;
	int size;
	int depth;
	int label;
	bool terminal;
	vector<int> indexes;
	vector<node *> child;
}*root;    

class form_tree{
public:
	node* main_func(string str);
	void main_function(string parse_quest);
	void depth(node *t ,int dpt);
	int size(node *t);
	void size1(node *t);
	void level_order(node *t);
	void assign_child(node *t);
	int total_fragments(node *t);
	node* get(node *t,int pos);
	void delta(string str);
	void calculate(node *t1,node *t2);
};


node* form_tree::main_func(string str){
	stack<node *> stk;
	node *temp = new node;
	stringstream ss;
	ss << str[0];
 	ss >> temp->str;
	stk.push(temp);
	string str2 = ""; 
	
	cout << str << endl;
	cout << stk.top() -> str << endl;
	for(int i=1;i<str.length();i++){
	if(stk.size() == 10){
			cout << "iam herh";
			while(!stk.empty()){
				node * temp5 = stk.top();
				cout << temp5 -> str << endl;
				stk.pop();
			}
		}

	if(str[i] == ')' || str[i] == '('){
			if(str[i] == ')'){
				if(str2 != ""){
					node *temp4 = new node;
					temp4 -> str = str2;
					temp4->size = 0;
					temp4->label = -1;
					temp4->depth = 0;
					temp4->terminal = false;
					str2 = "";
					stk.push(temp4);
				}

				cout << "after I" << endl;
 				vector<node *> children;

				while(!stk.empty()){
					node *temp5 = stk.top();
					cout << "top of the stack: " << temp5->str << endl;
					stk.pop();
					if(temp5->str == "("){
						cout << "ima";
						break;
					}
					else
						children.push_back(temp5);
				}
				node *temp3;
				int sz = children.size()-1;
				cout << sz << endl;
				temp3 -> str = children[sz]->str;
				for(int j=0;j<children.size()-1;j++)
					temp3 -> child.push_back(children[j]);
				temp3->size = 0;
				temp3->label = -1;
				temp3->depth = 0;
				temp3->terminal = false;
				stk.push(temp3);
			}
			else{
				node *temp2;
				stringstream ss2;
				ss2 << str[i]; 
				ss2 >> temp2->str;
				cout << "in open: "<< temp2 -> str << endl;
				temp2->size = 0;
				temp2->label = -1;
				temp2->depth = 0;
				temp2->terminal = false;
				stk.push(temp2);
				cout << "stack top: " << stk.top() -> str << endl;
			}
		}
		else{
			if(str[i] != ' '){
				str2 = str2 + str[i];
				cout << "string was: " << str2 << endl;
			}
			else{
				node *temp2;
				temp2 -> str = str2;
				temp2->size = 0;
				temp2->label = -1;
				temp2->depth = 0;
				temp2->terminal = false;
				stk.push(temp2);
				cout << stk.top() -> str << endl;
				str2 = "";
			}
		}
	}
	node *t1 = stk.top();
	return t1;
}


void form_tree::main_function(string parse_quest){
	node *t = new node();
	t=main_func(parse_quest);
}
/*
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


//Main part comes here
//calculating M(r1,r2)


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

*/

int main(int argc,char *argv[]){
	zmq::context_t context (1);
	zmq::socket_t socket (context, ZMQ_REP);
	socket.bind ("tcp://127.0.0.1:5000");
	form_tree obj;
	string parse_quest = "(ROOT (S (S (NP (PRP I)) (VP (VBP am) (NP (NNP CA)))) (, ,) (NP (PRP I)) (VP (VBP wan) (S (VP (TO na) (VP (VB do) (NP (DT any) (NN rcgnzd) (NN course)) (PP (IN for) (S (VP (VBG entering) (PP (IN in) (NP (NN share) (NN market)))))))))) (. .)))";
	obj.main_function(parse_quest);
/*
	while (true) {
		cout<<"iam here"<<endl;
        zmq::message_t request,request2;
        socket.recv (&request);
        cout <<"iam here tweoooo"<<endl;
		char *num = (char *) request.data();
        string parse_quest = "";

        int i;
       	for(i=0;i<strlen(num);i++){
        	if(num[i] == '\n')
        		break;
        	parse_quest = parse_quest + num[i];
        }
        cout << parse_quest << endl;

        vector<int> train_quest;
        int val = 0;
        for(int j=i;j<strlen(num);j++){
        	if(num[j] == '$'){
        		train_quest.push_back(val);
        		val = 0;
        	}
        	else
        		val = val * 10 + (int)(num[j] - '0');
        }
        cout << train_quest.size() << endl;
        obj.main_function(parse_quest);
        sleep (1000);
    }
    return 0;
*/
}