#include "mongo/client/dbclient.h"
#include <stdio.h>
#include <cstdlib>
#include <stdlib.h>
#include <iostream>

#include <time.h>
#define ID_LEN         24
#define N_CHILD        36

#define timing(f) {long t = cur_ms(); f; printf("Elapsed time is: %lds\n", cur_ms() - t);}

using std::vector;
using std::string;
using std::auto_ptr;

long
cur_ms()
{
    struct timespec t_spec;

    clock_gettime(CLOCK_REALTIME, &t_spec);
    return t_spec.tv_sec * 1000 + t_spec.tv_nsec / 1000000;
}

int
get_idx(char c)
{
    if (c >= '0' && c <= '9')
        return c - '0';
    return c - 'A' + 10;
}

class S_List {
public:
    S_List	*next;
    string	*id;

    S_List(string *id, S_List *next);
    ~S_List(void);

    S_List *concat(S_List *olist);
};

void
pr_ids(S_List *ids)
{
    for (S_List *id = ids; id != NULL; id = id->next)
        printf("%s\t", id->id->c_str());
        //std::cout <<  *(id->id) << '\t';
    putchar('\n');
    //std::cout << std::endl;
}

S_List *
S_List::concat(S_List *olist)
{
    for (S_List *ilist = this; ilist->next != NULL || (ilist->next = olist); ilist=ilist->next);
    return this;
}

S_List::~S_List(void)
{
    //std::cout << "OH! I'm dead! ======== S_List" << std::endl;
    //delete this->id;
    pr_ids(this);
    for (; this->next != NULL; this->next = this->next->next) {
        //free(this->next->id);
        printf("is that good, ==== %p\n", this->next);
        std::cout << *this->next->id << std::endl;
        free(this->next);
    }
        printf("is that good 2\n");
    //if (this->next != NULL)
    //delete this->next;
}

S_List::S_List(string *id, S_List *next)
{
    this->id = id;
    this->next = next;
}

class Py_Tree {
public:
    Py_Tree                 *next[N_CHILD];
    S_List                 *ids;
    
    Py_Tree(void);
    ~Py_Tree(void);

    Py_Tree *make_node(void);        
    void fresh(string *py, string *id);
    void add_Id(string *id);
    Py_Tree *search(const char *s);
    Py_Tree *search(string s);
    S_List 	*get_all_ids(void);
    S_List	*get_all_ids(S_List *&ids);
};

S_List *
Py_Tree::get_all_ids(S_List *&ids)
{
    for (S_List *ilist = this->ids; ilist != NULL; ilist = ilist->next) {
        ids = new S_List(ilist->id, ids);
    }

    for (int i = 0; i < N_CHILD; i++) {
        Py_Tree *pt = this->next[i];
        pt && pt->get_all_ids(ids);
    }
    return ids;
}

S_List *
Py_Tree::get_all_ids(void)
{
    S_List *l = NULL;
    this->get_all_ids(l);
    return l;
}

Py_Tree *
Py_Tree::search(const char *s)
{
    Py_Tree *itree = this;
    for (int i = 0, len = strlen(s); i < len; i++) {
        itree = itree->next[get_idx(s[i])];
        if (itree == NULL)
            return NULL;
    }

    return itree;
}

Py_Tree *
Py_Tree::search(string s)
{
    return this->search(s.c_str());
}

void
Py_Tree::add_Id(string *id)
{
    this->ids = new S_List(id, this->ids);
}

Py_Tree::~Py_Tree(void)
{
    //std::cout << "OH! I'm dead!" << std::endl;
    delete this->ids;

    std::cout << "OH! I'm dead!" << std::endl;
    for (int i = 0; i < N_CHILD; i++)
        if (this->next[i] != NULL)
            delete this->next[i];
}

Py_Tree::Py_Tree(void)
{
    for (int i = 0; i < N_CHILD; i++)
            next[i] = NULL;
    ids = NULL;
}


Py_Tree *
Py_Tree::make_node(void)
{
    return new Py_Tree();
}

void
Py_Tree::fresh(string *py, string *id)
{
    if (id->length() != 24) {
        std::cout << "[ERROR in Py_Tree::fresh()]: Bad id -> " << id << std::endl;
        return;
    }

    Py_Tree *itree, *node;
    for (int len = py->length(), i = len - 1; i >= 0; i--) {
        itree = this;
        for (int j = i; j < len; j++) {
            int idx = get_idx(py->at(j));
            node = itree;
            if ((itree = itree->next[idx]) == NULL)
                itree = node->next[idx] = new Py_Tree();
        }
        itree->add_Id(id);
    }
}

void
pr_tree(Py_Tree *tree)
{
    if (tree == NULL)
        return;

    //printf("good\n");
    for (int i = 0; i < N_CHILD; i++) {
        if (tree->next[i] != NULL) {
            printf("%d\n", i);
            pr_tree(tree->next[i]);
        }
    }

    pr_ids(tree->ids);
}

void
foo(void)
{
    static int x = 0;
    printf("%d\n", x++);
    foo();
}
int
main(int argc, char *argv[])
{
    //foo();
    //S_List *list; 
    //for (int i = 0; i < 500000; i++) {
    //    list = new S_List(new string("abc"), list);
    //}
    //printf("good news\n");
    ////sleep(5);
    //delete list;

    Py_Tree *pt = new Py_Tree();

    std::cout << cur_ms() << std::endl;
#define host "localhost"
#define db string("newhao123")
    mongo::DBClientConnection mc;
    mc.connect(host);
    int cnt = mc.count(db + ".pinyin_index");
    std::cout << cnt << std::endl;

    auto_ptr<mongo::DBClientCursor> cursor = mc.query(db+".pinyin_index");
    char *is = new char[2];
    while (cursor->more()) {
        mongo::BSONObj item = cursor->next();
        //std::cout << item.getField("_id").__oid().toString() << std::endl;
        string *_id = new string(item.getField("_id").__oid().toString());
        //std::cout << item.getStringField("title") << std::endl;
        mongo::BSONObj py = item.getObjectField("pinyin");
        for (int i = 0; ; i++) {
            sprintf(is, "%d", i);
            string *s = new string(py.getStringField(is));
            if (s->empty()) {
                delete s;
                break;
            }
            pt->fresh(s, _id);
            delete s;
        }
        //std::cout << (strlen(item.getObjectField("pinyin").getStringField("3"))) << std::endl;
        //std::cout << item.toString() << std::endl;
    }

    delete is;

    //timing(pr_tree(pt->search(argv[1])));
    for (int i = 1; i < argc; i++) {
        Py_Tree *ipt = pt->search(argv[i]);
        timing(if (ipt != NULL) ipt->get_all_ids());
    }
    //pt->fresh(new string("goodnews"), new string("egfdegfdegfdegfdegfdegfd"));
    //pr_tree(pt);
    //std::cout << *pt->next[24]->next[24]->next[13]->next[23]->next[14]->next[32]->next[28]->ids->id << std::endl;
    //sleep(10);
    delete pt;
    return 0;
}
