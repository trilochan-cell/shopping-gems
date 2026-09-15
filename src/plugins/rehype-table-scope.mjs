import { visit } from 'unist-util-visit';

/** Adds scope="col" to <th> for screen-reader table navigation. */
export default function rehypeTableScope() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName === 'th') {
        node.properties = node.properties ?? {};
        node.properties.scope = 'col';
      }
    });
  };
}
