import React, { useState } from 'react';
import { useStory } from '../context/StoryContext';
import CorpusSymbol from './CorpusSymbol';
import VaultTree from './VaultTree';
import { corpusColors } from '../assets/colors';
import { StoryPage } from '../types/story';
import { BOOK_SECTIONS } from '../types/sections';

export function VaultIndex() {
  const { pages, currentPageIndex, furthestPageIndex, setCurrentPageIndex, getBranchTree, navigateToSection, getCurrentSection, getAccessibleSections } = useStory();
  const [viewMode, setViewMode] = useState<'grid' | 'tree' | 'toc'>('grid');
  
  // Get pages up to furthest unlocked - ensure we always show at least current page
  const maxPageIndex = Math.max(furthestPageIndex, currentPageIndex);
  const unlockedPages = pages.slice(0, maxPageIndex + 1);
  
  // Get accessible sections for TOC view
  const accessibleSections = getAccessibleSections();
  const currentSection = getCurrentSection();

  const VaultPageCell: React.FC<{ page: StoryPage; index: number }> = ({ page, index }) => {
    const color = corpusColors[page.symbolId] || '#34FF78';
    const isActive = currentPageIndex === index;
    const branches = getBranchTree(page.id);
    const hasRotation = page.rotation !== 0;
    
    return (
      <div className="vault-page-cell relative">
        <button
          onClick={() => setCurrentPageIndex(index)}
          className={`
            flex flex-col items-center p-2 rounded transition-all duration-200 min-w-0 w-full aspect-square relative
            ${isActive 
              ? 'transform scale-105' 
              : 'hover:bg-opacity-10'
            }
          `}
          style={{
            backgroundColor: isActive ? 'transparent' : 'transparent',
            borderColor: color,
            borderWidth: isActive ? '2px' : '1px',
            borderStyle: 'solid',
            boxShadow: isActive ? `0 0 15px ${color}, 0 0 30px ${color}66` : 'none'
          }}
        >
          {/* Rotation Indicator */}
          <div
            className="transition-transform duration-500"
            style={{ transform: `rotate(${page.rotation}deg)` }}
          >
            <CorpusSymbol symbolId={page.symbolId} color={color} size="20px" />
          </div>
          
          {/* Page Number */}
          <span 
            className="font-mono text-xs mt-1"
            style={{ color }}
          >
            {index + 1}
          </span>
          
          {/* Branch Indicator */}
          {branches.length > 0 && (
            <div 
              className="absolute -top-1 -right-1 w-3 h-3 rounded-full flex items-center justify-center"
              style={{ 
                backgroundColor: color,
                color: '#0a0a0a'
              }}
            >
              <span className="text-xs font-mono font-bold">{branches.length}</span>
            </div>
          )}
          
          {/* Rotation State Indicator */}
          {hasRotation && (
            <div 
              className="absolute -bottom-1 -left-1 w-4 h-1 rounded-full"
              style={{ 
                backgroundColor: color,
                opacity: 0.7
              }}
            />
          )}
        </button>
        
        {/* Branch Tree (in tree view mode) */}
        {viewMode === 'tree' && branches.length > 0 && (
          <div className="branch-connections mt-2 pl-2 border-l-2 border-opacity-30" 
               style={{ borderColor: color }}>
            {branches.map((branch, branchIndex) => (
              <div 
                key={branch.pageId}
                className="branch-node flex items-center gap-2 py-1"
              >
                <div 
                  className="w-2 h-2 rounded-full"
                  style={{ 
                    backgroundColor: branch.createdBy === 'user' ? color : `${color}80`
                  }}
                />
                <span 
                  className="text-xs font-mono opacity-70"
                  style={{ color }}
                >
                  {branch.createdBy === 'user' ? '👤' : '🤖'} {branchIndex + 1}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const SectionCell: React.FC<{ section: any; isActive: boolean }> = ({ section, isActive }) => {
    const color = corpusColors[section.symbolId] || '#34FF78';
    const hasBeenAccessed = furthestPageIndex >= (section.startPage - 1);
    
    return (
      <div className="section-cell relative mb-2">
        <button
          onClick={() => navigateToSection(section.id)}
          className={`
            flex flex-col items-start p-3 rounded transition-all duration-200 w-full text-left hover:bg-opacity-10 cursor-pointer
            ${isActive ? 'transform scale-105' : ''}
          `}
          style={{
            backgroundColor: 'transparent',
            borderColor: color,
            borderWidth: isActive ? '2px' : '1px',
            borderStyle: 'solid',
            boxShadow: isActive ? `0 0 15px ${color}, 0 0 30px ${color}66` : `0 0 5px ${color}40`,
            opacity: hasBeenAccessed ? 1 : 0.7
          }}
        >
          {/* Section Symbol */}
          <div className="flex items-center gap-2 mb-2">
            <CorpusSymbol symbolId={section.symbolId} color={color} size="16px" />
            <span 
              className="font-mono text-sm font-bold"
              style={{ color }}
            >
              Section {section.id}
            </span>
          </div>
          
          {/* Section Title */}
          <h3 
            className="font-crt text-sm mb-1 leading-tight"
            style={{ color }}
          >
            {section.title}
          </h3>
          
          {/* Character Name */}
          <p 
            className="text-xs opacity-70 mb-2"
            style={{ color }}
          >
            {section.character}
          </p>
          
          {/* Page Range */}
          <div 
            className="text-xs font-mono opacity-60"
            style={{ color }}
          >
            Pages {section.startPage}-{section.endPage} ({section.totalPages} pages)
          </div>
          
          {/* Progress indicator */}
          <div className="mt-2 w-full">
            <div className="w-full h-1 bg-gray-800 rounded overflow-hidden">
              <div 
                className="h-full transition-all duration-500"
                style={{ 
                  width: hasBeenAccessed ? `${Math.min(100, Math.max(0, ((furthestPageIndex + 1 - section.startPage + 1) / section.totalPages) * 100))}%` : '0%',
                  backgroundColor: color
                }}
              />
            </div>
            <div className="text-xs font-mono opacity-50 mt-1" style={{ color }}>
              {hasBeenAccessed ? 'Accessed' : 'Available'}
            </div>
          </div>
        </button>
      </div>
    );
  };

  return (
    <div className="space-y-2 w-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-mono text-center flex-1">
          GIBSEY VAULT
        </h2>
        <div className="flex gap-1">
          <button
            onClick={() => setViewMode('grid')}
            className={`px-2 py-1 text-xs font-mono border transition-all ${
              viewMode === 'grid' ? 'bg-opacity-20' : 'opacity-50'
            }`}
            style={{ 
              borderColor: '#34FF78',
              color: '#34FF78',
              backgroundColor: viewMode === 'grid' ? '#34FF7820' : 'transparent'
            }}
          >
            GRID
          </button>
          <button
            onClick={() => setViewMode('tree')}
            className={`px-2 py-1 text-xs font-mono border transition-all ${
              viewMode === 'tree' ? 'bg-opacity-20' : 'opacity-50'
            }`}
            style={{ 
              borderColor: '#34FF78',
              color: '#34FF78',
              backgroundColor: viewMode === 'tree' ? '#34FF7820' : 'transparent'
            }}
          >
            TREE
          </button>
          <button
            onClick={() => setViewMode('toc')}
            className={`px-2 py-1 text-xs font-mono border transition-all ${
              viewMode === 'toc' ? 'bg-opacity-20' : 'opacity-50'
            }`}
            style={{ 
              borderColor: '#34FF78',
              color: '#34FF78',
              backgroundColor: viewMode === 'toc' ? '#34FF7820' : 'transparent'
            }}
          >
            TOC
          </button>
        </div>
      </div>
      
      <div className="h-[60vh] overflow-y-auto w-full custom-scrollbar px-2" style={{ scrollBehavior: 'smooth' }}>
        {viewMode === 'grid' ? (
          <div className="grid grid-cols-3 gap-2 auto-rows-min pb-6">
            {unlockedPages.map((page, index) => (
              <VaultPageCell key={`page-${index}`} page={page} index={index} />
            ))}
          </div>
        ) : viewMode === 'tree' ? (
          <div className="pb-6">
            <VaultTree 
              pages={unlockedPages} 
              currentPageIndex={currentPageIndex}
            />
          </div>
        ) : (
          <div className="space-y-2 pb-6">
            {BOOK_SECTIONS.map((section) => {
              const isActive = currentSection?.id === section.id;
              return (
                <SectionCell 
                  key={`section-${section.id}`} 
                  section={section} 
                  isActive={isActive}
                />
              );
            })}
          </div>
        )}
      </div>
      
      <div className="mt-4 pt-4 border-t border-current border-opacity-20">
        <div className="flex justify-between items-center text-xs font-mono opacity-50">
          <span>{furthestPageIndex + 1} / {pages.length} pages</span>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-current rounded-full opacity-70" />
              <span>Rotated</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-current rounded-full flex items-center justify-center">
                <span className="text-xs">N</span>
              </div>
              <span>Branches</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}