#include "apue.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define  LEN 36

struct list {
    struct list     *next;
    char            *id;
};

typedef struct py_tree {
    struct py_tree  *next[LEN];
    struct list     *ids;
} py_tree;

//py_tree tree[26];


py_tree *
make_node()
{
    py_tree *node = (py_tree *) malloc(sizeof(struct py_tree));
    for (int i = 0; i < LEN; i++)
	node->next[i] = NULL;
    node->ids = NULL;
    return node;
}

py_tree *tree; 

void
free_tree(py_tree *tree)
{
    for (struct list *id = tree->ids; id != NULL;) {
	struct list *next = id->next;
	free(id);
	id = next;
    }

    for (int i = 0; i < LEN; i++)
	if (tree->next[i] != NULL)
	    free_tree(tree->next[i]);
    free(tree);
}

int
get_idx(char c)
{
    if (c >= '0' && c <= '9')
	return c - '0';
    return c - 'a' + 10;
}

struct list *
add2list(struct list *ids, char *s)
{
    struct list *ilist = (struct list *) malloc(sizeof(struct list));
    ilist->id = s;
    ilist->next = ids;
    return ilist;
}

void
push2tree(char *py, char *id)
{
    if (strlen(id) != 24) {
	err_ret("bad id");
	return;
    }

    py_tree *itree, *node;
    int py_len = strlen(py);
    for (int i = py_len - 1; i >= 0; i--) {
	itree = tree;
	for (int j = i; j < py_len; j++) {
	    node = itree;
	    itree = itree->next[get_idx(py[j])];
	    if (itree == NULL)
		itree = node->next[get_idx(py[j])] = make_node();
	}
	itree->ids = add2list(itree->ids, id);
    }
}

void
pr_ids(struct list *ids)
{
    for (struct list *id = ids; id != NULL; id = id->next)
	printf("%s\t", id->id);
    putchar('\n');
}

void
pr_tree(py_tree *tree)
{
    if (tree == NULL)
	return;

    //printf("good\n");
    for (int i = 0; i < LEN; i++) {
	if (tree->next[i] != NULL) {
	    printf("%d\n", i);
	    pr_tree(tree->next[i]);
	}
    }

    pr_ids(tree->ids);
}

int
main(void)
{
    sleep(10);
    tree = make_node();

    push2tree("abc", "abcabcabcabcabcabcabcabc");
    push2tree("aac", "edgabcabcabcabcabcabcabc");
    pr_tree(tree);

    //printf("%d\n", get_idx('z'));

    free_tree(tree);
    sleep(10);
    return 0;
}
