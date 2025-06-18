import React from 'react';
import { StoryPage } from '../types/story';
import { useStory } from '../context/StoryContext';
import { corpusColors } from '../assets/colors';
import CorpusSymbol from './CorpusSymbol';

interface VaultTreeProps {
  pages: StoryPage[];
  currentPageIndex: number;
}

interface TreeNode {
  page: StoryPage;
  index: number;
  children: TreeNode[];
  level: number;
  isActive: boolean;
}

const VaultTree: React.FC<VaultTreeProps> = ({ pages, currentPageIndex }) => {
  const { setCurrentPageIndex, getBranchTree } = useStory();

  // Build tree structure from pages
  const buildTree = (): TreeNode[] => {
    const nodeMap = new Map<string, TreeNode>();
    const rootNodes: TreeNode[] = [];

    // Create nodes for all pages
    pages.forEach((page, index) => {
      const node: TreeNode = {
        page,
        index,
        children: [],
        level: 0,
        isActive: currentPageIndex === index
      };
      nodeMap.set(page.id, node);
    });

    // Build parent-child relationships
    pages.forEach((page) => {
      const node = nodeMap.get(page.id);
      if (!node) return;

      if (page.parentId) {
        const parent = nodeMap.get(page.parentId);
        if (parent) {
          node.level = parent.level + 1;
          parent.children.push(node);
        }
      } else {
        // This is a root node (primary story page)
        rootNodes.push(node);
      }
    });

    return rootNodes;
  };

  const renderTreeNode = (node: TreeNode): JSX.Element => {
    const color = corpusColors[node.page.symbolId] || '#34FF78';
    const branches = getBranchTree(node.page.id);
    
    return (
      <div key={node.page.id} className="tree-node">
        {/* Node Content */}
        <div 
          className={`flex items-center gap-3 p-2 rounded-sm cursor-pointer transition-all duration-200 ${
            node.isActive ? 'scale-105' : 'hover:bg-opacity-10'
          }`}
          style={{
            marginLeft: `${node.level * 20}px`,
            borderLeft: node.level > 0 ? `2px solid ${color}40` : 'none',
            paddingLeft: node.level > 0 ? '12px' : '0',
            backgroundColor: node.isActive ? `${color}20` : 'transparent',
            borderColor: node.isActive ? color : 'transparent',
            borderWidth: node.isActive ? '1px' : '0',
            boxShadow: node.isActive ? `0 0 15px ${color}40` : 'none'
          }}
          onClick={() => setCurrentPageIndex(node.index)}
        >
          {/* Connection Line for Children */}
          {node.level > 0 && (
            <div 
              className="absolute w-4 h-0.5"
              style={{
                backgroundColor: `${color}60`,
                left: `${node.level * 20 - 8}px`,
                marginTop: '8px'
              }}
            />
          )}

          {/* Symbol with Rotation */}
          <div
            className="transition-transform duration-500 flex-shrink-0"
            style={{ transform: `rotate(${node.page.rotation}deg)` }}
          >
            <CorpusSymbol 
              symbolId={node.page.symbolId} 
              color={color} 
              size="16px"
            />
          </div>

          {/* Page Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs" style={{ color }}>
                {node.index + 1}
              </span>
              <span className="font-crt text-xs opacity-70" style={{ color }}>
                {node.page.pageType}
              </span>
              {node.page.rotation !== 0 && (
                <span className="font-mono text-xs opacity-50" style={{ color }}>
                  {node.page.rotation}°
                </span>
              )}
            </div>
            
            <div className="font-crt text-xs mt-1 truncate" style={{ color }}>
              {node.page.pageType === 'primary' ? node.page.title : `${node.page.author}: ${node.page.text.slice(0, 40)}...`}
            </div>
          </div>

          {/* Branch Count */}
          {branches.length > 0 && (
            <div 
              className="w-5 h-5 rounded-full flex items-center justify-center text-xs font-mono font-bold"
              style={{ 
                backgroundColor: color,
                color: '#0a0a0a'
              }}
            >
              {branches.length}
            </div>
          )}

          {/* Page Type Indicator */}
          <div 
            className="w-2 h-2 rounded-full"
            style={{ 
              backgroundColor: getPageTypeColor(node.page.pageType, color)
            }}
          />
        </div>

        {/* Render Children */}
        {node.children.length > 0 && (
          <div className="tree-children">
            {node.children.map(childNode => renderTreeNode(childNode))}
          </div>
        )}
      </div>
    );
  };

  const getPageTypeColor = (pageType: string, baseColor: string): string => {
    switch (pageType) {
      case 'primary': return baseColor;
      case 'user_query': return '#00aaff';
      case 'ai_response': return '#ff6600';
      case 'prompt': return '#aa00ff';
      default: return baseColor;
    }
  };

  const treeNodes = buildTree();

  return (
    <div className="vault-tree space-y-1">
      <div className="tree-legend mb-4 p-3 border rounded-sm border-opacity-30">
        <div className="text-xs font-crt mb-2 opacity-70">NARRATIVE TREE LEGEND</div>
        <div className="grid grid-cols-2 gap-2 text-xs font-crt">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-current" />
            <span className="opacity-70">Primary Story</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#00aaff' }} />
            <span className="opacity-70">User Query</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#ff6600' }} />
            <span className="opacity-70">AI Response</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#aa00ff' }} />
            <span className="opacity-70">Character Prompt</span>
          </div>
        </div>
      </div>

      <div className="tree-structure mb-4">
        {treeNodes.map(node => renderTreeNode(node))}
      </div>

      {treeNodes.length === 0 && (
        <div className="text-center py-8 opacity-50">
          <div className="text-sm font-crt">
            No narrative tree structure found
          </div>
        </div>
      )}
    </div>
  );
};

export default VaultTree;